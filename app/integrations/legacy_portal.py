from dataclasses import dataclass

from playwright.sync_api import sync_playwright

from app.config import settings


@dataclass(frozen=True)
class PortalOrder:
    status: str
    quantity: int


class LegacyPortalClient:
    def fetch_order(self, order_id: str) -> PortalOrder:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(settings.portal_base_url, wait_until="domcontentloaded")
                page.locator("#username").fill(settings.portal_username)
                page.locator("#password").fill(settings.portal_password)
                page.locator("button[type='submit']").click()
                page.locator("#order-search").fill(order_id)
                page.locator("#search-button").click()
                page.wait_for_selector("#order-status", timeout=10_000)
                status = page.locator("#order-status").inner_text().strip()
                quantity = int(page.locator("#order-quantity").inner_text().strip())
                return PortalOrder(status=status, quantity=quantity)
            finally:
                browser.close()
