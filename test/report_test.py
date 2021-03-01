import shopify
from test.test_helper import TestCase


class CustomerSavedSearchTest(TestCase):
    def test_get_report(self):
        self.fake("reports/987", method="GET", code=200, body=self.load_fixture("report"))
        report = shopify.Report.find(987)
        self.assertEqual(987, report.id)

    def test_get_reports(self):
        self.fake("reports", method="GET", code=200, body=self.load_fixture("reports"))
        reports = shopify.Report.find()
        self.assertEqual("custom_app_reports", reports[0].category)

    def test_create_report(self):
        self.fake(
            "reports",
            method="POST",
            code=201,
            body=self.load_fixture("report"),
            headers={"Content-type": "application/json"},
        )
        report = shopify.Report.create(
            {
                "name": "Custom App Report",
                "shopify_ql": "SHOW quantity_count, total_sales BY product_type, vendor, product_title FROM products SINCE -1m UNTIL -0m ORDER BY total_sales DESC",
            }
        )
        self.assertEqual("custom_app_reports", report.category)

    def test_delete_report(self):
        self.fake("reports/987", method="GET", code=200, body=self.load_fixture("report"))
        self.fake("reports", method="DELETE", code=200, body="[]")
        report = shopify.Report.find(987)
        self.assertTrue(report.destroy)
