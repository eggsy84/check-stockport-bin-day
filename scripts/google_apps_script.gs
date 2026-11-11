/**
 * Stockport Council Bin Collection — Google Account Live Lookup & Gemini Integration
 *
 * How to set up in your Google Account (takes 2 minutes):
 * 1. Go to https://script.google.com and click "New project".
 * 2. Paste this entire file into Code.gs.
 * 3. Set your Stockport UPRN below (find it by entering your postcode at
 *    https://www.stockport.gov.uk/find-your-collection-day — the number at the end
 *    of the URL https://myaccount.stockport.gov.uk/bin-collections/show/10090543805
 *    is your UPRN).
 * 4. For Live On-Demand Webhook:
 *    Click "Deploy" -> "New deployment" -> Select type "Web app" ->
 *    Execute as "Me", Who has access "Anyone" -> Deploy.
 * 5. For Nest Speaker / Gemini Voice ("Hey Google, what bin should I put out?"):
 *    Run `setupWeeklyTrigger()` once in the Apps Script editor. It will keep your
 *    Google Calendar populated with live Stockport Council bin days so Gemini can
 *    answer via @Google Calendar on phone, web, and Nest speakers.
 */

const STOCKPORT_UPRN = 'REPLACE_WITH_YOUR_UPRN'; // e.g. '10090543805'

/**
 * Live lookup of Stockport Council bin schedule on demand.
 */
function fetchStockportBins(uprn) {
  const cleanUprn = String(uprn || STOCKPORT_UPRN).trim().split('/').pop();
  if (!/^\d+$/.test(cleanUprn)) {
    throw new Error(
      'Please set STOCKPORT_UPRN to your numeric UPRN from https://myaccount.stockport.gov.uk/bin-collections/show/<UPRN>'
    );
  }

  const url = `https://myaccount.stockport.gov.uk/bin-collections/show/${cleanUprn}`;
  const response = UrlFetchApp.fetch(url, {
    muteHttpExceptions: true,
    headers: {
      'User-Agent': 'Mozilla/5.0 (compatible; StockportBinSkill/1.0)',
      'Accept': 'text/html'
    }
  });

  if (response.getResponseCode() !== 200) {
    throw new Error(`Stockport Council returned HTTP ${response.getResponseCode()}`);
  }

  const html = response.getContentText();
  // Strip tags into clean text lines
  const text = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<\/(div|p|h1|h2|h3|h4|li|tr)>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, ' ')
    .replace(/[ \t]+/g, ' ');

  const lines = text
    .split('\n')
    .map(l => l.trim())
    .filter(Boolean);

  const binTypes = ['Black bin', 'Blue bin', 'Brown bin', 'Green bin'];
  const dateRegex = /(?:(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+)?(\d{1,2}\s+[A-Za-z]+\s+\d{4})/i;

  const collections = [];
  const seen = {};

  for (let i = 0; i < lines.length; i++) {
    const matchedBin = binTypes.find(b =>
      lines[i].toLowerCase().startsWith(b.toLowerCase())
    );
    if (matchedBin && !seen[matchedBin]) {
      const windowText = lines.slice(i, i + 4).join(' | ');
      const match = windowText.match(dateRegex);
      if (match) {
        const parsedDate = new Date(match[1]);
        if (!isNaN(parsedDate.getTime())) {
          seen[matchedBin] = true;
          collections.push({
            bin: matchedBin,
            dateString: match[0],
            isoDate: Utilities.formatDate(parsedDate, 'Europe/London', 'yyyy-MM-dd'),
            timestamp: parsedDate.getTime()
          });
        }
      }
    }
  }

  collections.sort((a, b) => a.timestamp - b.timestamp);

  if (collections.length === 0) {
    return {
      found: false,
      speech: 'I could not find any upcoming bin collections on the Stockport Council page.',
      collections: []
    };
  }

  const nextIsoDate = collections[0].isoDate;
  const nextDateReadable = collections[0].dateString;
  const nextBins = collections
    .filter(c => c.isoDate === nextIsoDate)
    .map(c => c.bin);

  const binsText =
    nextBins.length > 1
      ? nextBins.slice(0, -1).join(', ') + ' and ' + nextBins.slice(-1)
      : nextBins[0];

  const speech = `Your next bin collection is on ${nextDateReadable}. You should put out your ${binsText}.`;

  return {
    found: true,
    nextDate: nextIsoDate,
    nextDateReadable: nextDateReadable,
    binsToPutOut: nextBins,
    speech: speech,
    allCollections: collections
  };
}

/**
 * Live Web App endpoint (GET).
 * Supports ?uprn=10090543805&format=text (or JSON by default)
 */
function doGet(e) {
  try {
    const uprn = (e && e.parameter && e.parameter.uprn) || STOCKPORT_UPRN;
    const format = (e && e.parameter && e.parameter.format) || 'json';
    const result = fetchStockportBins(uprn);

    if (format === 'text') {
      return ContentService.createTextOutput(result.speech).setMimeType(
        ContentService.MimeType.TEXT
      );
    }
    return ContentService.createTextOutput(JSON.stringify(result, null, 2)).setMimeType(
      ContentService.MimeType.JSON
    );
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ error: err.message }, null, 2)
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Syncs live Stockport bin dates to your primary Google Calendar so Gemini on
 * phone, web, and Nest speakers can answer "What bin day is it?" or
 * "What bin should I put out?" natively.
 */
function syncBinsToCalendar() {
  const result = fetchStockportBins(STOCKPORT_UPRN);
  if (!result.found) return;

  const cal = CalendarApp.getDefaultCalendar();

  // Group bins by collection date
  const byDate = {};
  result.allCollections.forEach(item => {
    if (!byDate[item.isoDate]) byDate[item.isoDate] = [];
    byDate[item.isoDate].push(item.bin);
  });

  Object.keys(byDate).forEach(isoDate => {
    const bins = byDate[isoDate].join(' & ');
    const title = `Bin Day: Put out ${bins}`;
    const eventDate = new Date(isoDate + 'T00:00:00');

    // Avoid duplicate events on the same day
    const existing = cal.getEventsForDay(eventDate).filter(ev =>
      ev.getTitle().startsWith('Bin Day:')
    );
    existing.forEach(ev => ev.deleteEvent());

    cal.createAllDayEvent(title, eventDate, {
      description: `Stockport Council Bin Collection: Put out your ${bins}.`
    });
  });
}

/**
 * Run once to schedule automatic daily live lookups into your Google Calendar.
 */
function setupDailyTrigger() {
  ScriptApp.newTrigger('syncBinsToCalendar')
    .timeBased()
    .everyDays(1)
    .atHour(7)
    .create();
  syncBinsToCalendar();
}
