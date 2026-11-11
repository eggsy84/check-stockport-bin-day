import unittest
from datetime import date
from stockport_bins import StockportBinHTMLParser, parse_uk_date, summarize_next_collection


SAMPLE_STOCKPORT_HTML = """
<!DOCTYPE html>
<html>
<body>
  <div class="service-item service-item-blue-bin">
    <h3>Blue bin</h3>
    <p>Friday, 13 November 2026</p>
  </div>
  <div class="service-item service-item-brown-bin">
    <h3>Brown bin</h3>
    <p>Friday, 13 November 2026</p>
  </div>
  <div class="service-item service-item-black-bin">
    <h3>Black bin</h3>
    <p>Friday, 20 November 2026</p>
  </div>
  <div class="service-item service-item-green-bin">
    <h3>Green bin</h3>
    <p>Friday, 13 November 2026</p>
  </div>
</body>
</html>
"""


class TestStockportBins(unittest.TestCase):
    def test_parse_uk_date(self):
        d = parse_uk_date("Friday, 13 November 2026")
        self.assertEqual(d, date(2026, 11, 13))

    def test_html_parser_and_summary(self):
        parser = StockportBinHTMLParser()
        parser.feed(SAMPLE_STOCKPORT_HTML)
        parser.close()
        self.assertIn("Blue bin", parser.text_blocks)
        self.assertIn("Friday, 13 November 2026", parser.text_blocks)

        collections = [
            {
                "bin": "Blue bin",
                "date": "2026-11-13",
                "day_of_week": "Friday",
                "formatted_date": "Friday, 13 November 2026",
                "days_until": 2,
            },
            {
                "bin": "Brown bin",
                "date": "2026-11-13",
                "day_of_week": "Friday",
                "formatted_date": "Friday, 13 November 2026",
                "days_until": 2,
            },
            {
                "bin": "Black bin",
                "date": "2026-11-20",
                "day_of_week": "Friday",
                "formatted_date": "Friday, 20 November 2026",
                "days_until": 9,
            },
        ]
        summary = summarize_next_collection(collections)
        self.assertTrue(summary["found"])
        self.assertEqual(summary["bins_to_put_out"], ["Blue bin", "Brown bin"])
        self.assertIn("Blue bin and Brown bin", summary["message"])


if __name__ == "__main__":
    unittest.main()
