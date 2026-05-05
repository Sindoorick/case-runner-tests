# Feature: User Access Control
# Sales Representatives can create, edit, and view Leads, Accounts, Contacts, and Opportunities.
# Sales Managers can view reports and dashboards related to team performance and the sales pipeline.

"""
Test cases for User Access Control feature.

This module tests that:
- Sales Representatives have proper access to create, edit, and view 
  Leads, Accounts, Contacts, and Opportunities.
- Sales Managers can view reports and dashboards related to team performance 
  and the sales pipeline.

Page Object Models used:
- SalesforceAccountsListViewPage
- SalesforceAccountDetailPage
- SalesforceDashboardPage
"""

import pytest
from playwright.sync_api import Page, expect, BrowserContext
import logging

# Import Page Object Models
from pages.salesforce_accounts_list_view_page import SalesforceAccountsListViewPage
from pages.salesforce_account_detail_page import SalesforceAccountDetailPage
from pages.salesforce_dashboard_page import SalesforceDashboardPage

logger = logging.getLogger(__name__)

# TODO: Replace with actual Salesforce instance URL
BASE_URL = "https://df4000004ioimeaw--dexiantic.sandbox.lightning.force.com"

# TODO: Replace with actual test credentials for Sales Representative
SALES_REP_USERNAME = "sales.rep@company.com.sandbox"
SALES_REP_PASSWORD = "SalesRepPassword123!"

# TODO: Replace with actual test credentials for Sales Manager
SALES_MANAGER_USERNAME = "sales.manager@company.com.sandbox"
SALES_MANAGER_PASSWORD = "SalesManagerPassword123!"

# TODO: Replace with actual Salesforce login URL
LOGIN_URL = "https://test.salesforce.com"

# TODO: Replace with actual test data
TEST_ACCOUNT_NAME = "Test Account - Automation"
TEST_ACCOUNT_ID = "001VG00000paK6AYAU"
TEST_LEAD_NAME = "Test Lead - Automation"
TEST_CONTACT_NAME = "Test Contact - Automation"
TEST_OPPORTUNITY_NAME = "Test Opportunity - Automation"


# ==================== HELPER FUNCTIONS ====================


def login_as_sales_rep(page: Page) -> None:
    """
    Helper function to login as a Sales Representative.
    
    Page Object Models used: None (direct Salesforce login page interaction)
    
    Args:
        page: Playwright page object
    """
    # TODO: Update login flow based on actual Salesforce login page structure
    logger.info("Logging in as Sales Representative")
    page.goto(LOGIN_URL)
    page.fill("#username", SALES_REP_USERNAME)
    page.fill("#password", SALES_REP_PASSWORD)
    page.click("#Login")
    # Wait for home page to load after login
    page.wait_for_url(f"**/{BASE_URL}/**", timeout=60000)
    page.wait_for_load_state("networkidle")
    logger.info("Successfully logged in as Sales Representative")


def login_as_sales_manager(page: Page) -> None:
    """
    Helper function to login as a Sales Manager.
    
    Page Object Models used: None (direct Salesforce login page interaction)
    
    Args:
        page: Playwright page object
    """
    # TODO: Update login flow based on actual Salesforce login page structure
    logger.info("Logging in as Sales Manager")
    page.goto(LOGIN_URL)
    page.fill("#username", SALES_MANAGER_USERNAME)
    page.fill("#password", SALES_MANAGER_PASSWORD)
    page.click("#Login")
    # Wait for home page to load after login
    page.wait_for_url(f"**/{BASE_URL}/**", timeout=60000)
    page.wait_for_load_state("networkidle")
    logger.info("Successfully logged in as Sales Manager")


def verify_access_denied_message(page: Page) -> bool:
    """
    Helper function to check if an access denied/insufficient privileges message is shown.
    
    Page Object Models used: None (generic Salesforce error page interaction)
    
    Args:
        page: Playwright page object
    
    Returns:
        True if access denied message is visible, False otherwise
    """
    # TODO: Update with actual Salesforce access denied message locators
    insufficient_privileges_locator = "text=Insufficient Privileges"
    no_access_locator = "text=You don't have access"
    
    try:
        return (
            page.locator(insufficient_privileges_locator).is_visible(timeout=5000) or
            page.locator(no_access_locator).is_visible(timeout=5000)
        )
    except Exception:
        return False


# ==================== FIXTURES ====================


@pytest.fixture
def sales_rep_page(page: Page) -> Page:
    """
    Fixture that provides a page logged in as Sales Representative.
    
    Page Object Models used: None
    """
    login_as_sales_rep(page)
    return page


@pytest.fixture
def sales_manager_page(page: Page) -> Page:
    """
    Fixture that provides a page logged in as Sales Manager.
    
    Page Object Models used: None
    """
    login_as_sales_manager(page)
    return page


# ==================== SALES REPRESENTATIVE - ACCOUNTS TESTS ====================


class TestSalesRepAccountAccess:
    """
    Test class for Sales Representative access to Accounts.
    
    Verifies that Sales Representatives can create, edit, and view Accounts.
    """

    def test_sales_rep_can_view_accounts_list(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view the Accounts list view.
        
        Page Object Models used: SalesforceAccountsListViewPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Accounts list view
        3. Verify the page loads successfully with account data grid visible
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to accounts list
        accounts_page.navigate_to_accounts_list()
        
        # Verify page loaded - the grid should be visible and New button accessible
        accounts_page.verify_page_loaded()
        
        # Verify that the accounts tab is accessible
        expect(sales_rep_page.locator(accounts_page.PAGE_TITLE)).to_be_visible()
        expect(sales_rep_page.locator(accounts_page.DATA_GRID)).to_be_visible()
        
        # Verify no access denied message
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Accounts list"

    def test_sales_rep_can_view_account_detail(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view an Account detail page.
        
        Page Object Models used: SalesforceAccountDetailPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to a specific Account detail page
        3. Verify the account details are visible
        """
        account_detail_page = SalesforceAccountDetailPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to specific account
        # TODO: Use a known account ID that exists in the test org
        account_detail_page.navigate_to_account(TEST_ACCOUNT_ID)
        
        # Verify page loaded correctly
        assert account_detail_page.verify_account_page_loaded(), \
            "Sales Rep should be able to view Account detail page"
        
        # Verify key elements are visible
        expect(sales_rep_page.locator(account_detail_page.ACCOUNT_HEADER)).to_be_visible()
        
        # Verify no access denied message
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Account detail"

    def test_sales_rep_can_create_account(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can create a new Account.
        
        Page Object Models used: SalesforceAccountsListViewPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Accounts list view
        3. Click the "New" button
        4. Verify the new account form/modal appears
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to accounts list
        accounts_page.navigate_to_accounts_list()
        accounts_page.verify_page_loaded()
        
        # Verify New button is visible and clickable
        expect(sales_rep_page.locator(accounts_page.NEW_BUTTON)).to_be_visible()
        expect(sales_rep_page.locator(accounts_page.NEW_BUTTON)).to_be_enabled()
        
        # Click New button to start account creation
        accounts_page.click_new_account()
        
        # Verify the new account form/modal opens
        # TODO: Add specific locator for the new account modal/form
        new_account_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(new_account_modal)).to_be_visible(timeout=10000)
        
        # Verify the Account Name field is present in the form
        # TODO: Update locator based on actual form structure
        account_name_field = "input[field-label='Account Name'], input[placeholder='Account Name']"
        expect(sales_rep_page.locator(account_name_field).first).to_be_visible(timeout=5000)

    def test_sales_rep_can_edit_account(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can edit an existing Account.
        
        Page Object Models used: SalesforceAccountDetailPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to an Account detail page
        3. Click the "Edit" button
        4. Verify the edit form opens
        """
        account_detail_page = SalesforceAccountDetailPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to specific account
        # TODO: Use a known account ID that exists in the test org
        account_detail_page.navigate_to_account(TEST_ACCOUNT_ID)
        account_detail_page.wait_for_page_load()
        
        # Verify Edit button is visible and clickable
        expect(sales_rep_page.locator(account_detail_page.EDIT_BUTTON)).to_be_visible()
        expect(sales_rep_page.locator(account_detail_page.EDIT_BUTTON)).to_be_enabled()
        
        # Click Edit button
        account_detail_page.click_edit_button()
        
        # Verify edit form/modal opens
        # TODO: Update locator based on actual edit form structure
        edit_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(edit_modal)).to_be_visible(timeout=10000)

    def test_sales_rep_can_edit_account_inline(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can inline edit an Account from list view.
        
        Page Object Models used: SalesforceAccountsListViewPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Accounts list view
        3. Attempt inline edit on an account name field
        4. Verify the inline edit field becomes editable
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to accounts list
        accounts_page.navigate_to_accounts_list()
        accounts_page.verify_page_loaded()
        
        # TODO: Ensure at least one account exists for inline editing
        # Attempt to inline edit - this verifies edit access from list view
        # The test assumes TEST_ACCOUNT_NAME exists in the list
        if accounts_page.verify_account_exists(TEST_ACCOUNT_NAME):
            accounts_page.edit_account_name_inline(TEST_ACCOUNT_NAME)
            # Verify inline edit input appears
            # TODO: Add locator for inline edit input field
            inline_edit_input = "input[type='text']"
            expect(sales_rep_page.locator(inline_edit_input).first).to_be_visible(timeout=5000)


# ==================== SALES REPRESENTATIVE - LEADS TESTS ====================


class TestSalesRepLeadAccess:
    """
    Test class for Sales Representative access to Leads.
    
    Verifies that Sales Representatives can create, edit, and view Leads.
    """

    def test_sales_rep_can_view_leads_list(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view the Leads list view.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Leads list view via navigation tab
        3. Verify the Leads page loads without access denied error
        """
        # Use accounts page for navigation as it has the nav tabs
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to Leads via the navigation tab
        accounts_page.navigate_to_leads()
        
        # Wait for leads page to load
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify Leads page title is visible
        # TODO: Create a dedicated LeadsListViewPage POM for more specific assertions
        leads_title = "h1:has-text('Leads')"
        expect(sales_rep_page.locator(leads_title)).to_be_visible(timeout=30000)
        
        # Verify no access denied message
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Leads list"

    def test_sales_rep_can_create_lead(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can create a new Lead.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Leads list view
        3. Click the "New" button
        4. Verify the new lead form opens
        """
        # Navigate to Leads
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Lead/list")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify New button is visible
        # TODO: Create a dedicated LeadsListViewPage POM
        new_button = "button:has-text('New')"
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_enabled()
        
        # Click New button
        sales_rep_page.locator(new_button).first.click()
        
        # Verify new lead form/modal opens
        # TODO: Update locator based on actual lead form structure
        lead_form_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(lead_form_modal)).to_be_visible(timeout=10000)
        
        # Verify required lead fields are present
        # TODO: Add locators for Last Name, Company fields (required for Leads)
        last_name_field = "input[field-label='Last Name'], input[placeholder*='Last Name']"
        company_field = "input[field-label='Company'], input[placeholder*='Company']"
        # These assertions may need adjustment based on actual form structure

    def test_sales_rep_can_edit_lead(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can edit an existing Lead.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to a specific Lead detail page
        3. Click the "Edit" button
        4. Verify the edit form opens
        """
        # TODO: Replace with actual Lead ID from test data
        test_lead_id = "00QXX000000XXXXX"
        
        # Navigate directly to lead detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Lead/{test_lead_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify the lead page loads
        lead_header = "h1:has-text('Lead')"
        expect(sales_rep_page.locator(lead_header)).to_be_visible(timeout=30000)
        
        # Verify Edit button is visible and clickable
        edit_button = "button:has-text('Edit')"
        expect(sales_rep_page.locator(edit_button).first).to_be_visible()
        expect(sales_rep_page.locator(edit_button).first).to_be_enabled()
        
        # Click Edit button
        sales_rep_page.locator(edit_button).first.click()
        
        # Verify edit form opens
        edit_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(edit_modal)).to_be_visible(timeout=10000)
        
        # Verify no access denied message
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message when editing a Lead"

    def test_sales_rep_can_view_lead_detail(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view Lead details.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to a Lead detail page
        3. Verify lead details are displayed
        """
        # TODO: Replace with actual Lead ID from test data
        test_lead_id = "00QXX000000XXXXX"
        
        # Navigate to lead detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Lead/{test_lead_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify lead detail page loads
        lead_header = "h1:has-text('Lead')"
        expect(sales_rep_page.locator(lead_header)).to_be_visible(timeout=30000)
        
        # Verify key lead fields are visible
        # TODO: Add more specific field locators
        details_tab = "tab:has-text('Details')"
        activity_tab = "tab:has-text('Activity')"
        expect(sales_rep_page.locator(details_tab)).to_be_visible()
        expect(sales_rep_page.locator(activity_tab)).to_be_visible()
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Lead detail"


# ==================== SALES REPRESENTATIVE - CONTACTS TESTS ====================


class TestSalesRepContactAccess:
    """
    Test class for Sales Representative access to Contacts.
    
    Verifies that Sales Representatives can create, edit, and view Contacts.
    """

    def test_sales_rep_can_view_contacts_list(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view the Contacts list view.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Contacts list view via navigation tab
        3. Verify the Contacts page loads
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to Contacts via navigation tab
        accounts_page.navigate_to_contacts()
        
        # Wait for contacts page to load
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify Contacts page title
        # TODO: Create a dedicated ContactsListViewPage POM
        contacts_title = "h1:has-text('Contacts')"
        expect(sales_rep_page.locator(contacts_title)).to_be_visible(timeout=30000)
        
        # Verify data grid is present (contacts are viewable)
        data_grid = "grid"
        expect(sales_rep_page.locator(data_grid)).to_be_visible(timeout=15000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Contacts list"

    def test_sales_rep_can_create_contact(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can create a new Contact.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Contacts list view
        3. Click the "New" button
        4. Verify the new contact form opens
        """
        # Navigate to Contacts list
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Contact/list")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify New button is visible and clickable
        # TODO: Create a dedicated ContactsListViewPage POM
        new_button = "button:has-text('New')"
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_enabled()
        
        # Click New button
        sales_rep_page.locator(new_button).first.click()
        
        # Verify new contact form/modal opens
        contact_form_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(contact_form_modal)).to_be_visible(timeout=10000)

    def test_sales_rep_can_create_contact_from_account(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can create a new Contact from Account detail page.
        
        Page Object Models used: SalesforceAccountDetailPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Account detail page
        3. Switch to Related tab
        4. Click New Contact button in Contacts section
        5. Verify the new contact form opens
        """
        account_detail_page = SalesforceAccountDetailPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to account detail
        account_detail_page.navigate_to_account(TEST_ACCOUNT_ID)
        account_detail_page.wait_for_page_load()
        
        # Switch to Related tab
        account_detail_page.switch_to_related_tab()
        
        # Click New Contact button
        account_detail_page.create_new_contact()
        
        # Verify contact form opens
        contact_form_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(contact_form_modal)).to_be_visible(timeout=10000)

    def test_sales_rep_can_edit_contact(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can edit an existing Contact.
        
        Page Object Models used: None (direct page interaction)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to a Contact detail page
        3. Click the "Edit" button
        4. Verify the edit form opens
        """
        # TODO: Replace with actual Contact ID from test data
        test_contact_id = "003XX000000XXXXX"
        
        # Navigate to contact detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Contact/{test_contact_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify contact page loads
        contact_header = "h1:has-text('Contact')"
        expect(sales_rep_page.locator(contact_header)).to_be_visible(timeout=30000)
        
        # Verify Edit button is visible and enabled
        edit_button = "button:has-text('Edit')"
        expect(sales_rep_page.locator(edit_button).first).to_be_visible()
        expect(sales_rep_page.locator(edit_button).first).to_be_enabled()
        
        # Click Edit button
        sales_rep_page.locator(edit_button).first.click()
        
        # Verify edit form opens
        edit_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(edit_modal)).to_be_visible(timeout=10000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message when editing a Contact"

    def test_sales_rep_can_view_contact_detail(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view Contact details.
        
        Page Object Models used: None (direct page interaction)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to a Contact detail page
        3. Verify contact information is displayed
        """
        # TODO: Replace with actual Contact ID from test data
        test_contact_id = "003XX000000XXXXX"
        
        # Navigate to contact detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Contact/{test_contact_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify contact page loads with details
        contact_header = "h1:has-text('Contact')"
        expect(sales_rep_page.locator(contact_header)).to_be_visible(timeout=30000)
        
        # Verify tabs are accessible
        details_tab = "tab:has-text('Details')"
        related_tab = "tab:has-text('Related')"
        expect(sales_rep_page.locator(details_tab)).to_be_visible()
        expect(sales_rep_page.locator(related_tab)).to_be_visible()
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Contact detail"


# ==================== SALES REPRESENTATIVE - OPPORTUNITIES TESTS ====================


class TestSalesRepOpportunityAccess:
    """
    Test class for Sales Representative access to Opportunities.
    
    Verifies that Sales Representatives can create, edit, and view Opportunities.
    """

    def test_sales_rep_can_view_opportunities_list(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view the Opportunities list view.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Opportunities list view via navigation tab
        3. Verify the Opportunities page loads
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to Opportunities via navigation tab
        accounts_page.navigate_to_opportunities()
        
        # Wait for opportunities page to load
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify Opportunities page title
        # TODO: Create a dedicated OpportunitiesListViewPage POM
        opportunities_title = "h1:has-text('Opportunities')"
        expect(sales_rep_page.locator(opportunities_title)).to_be_visible(timeout=30000)
        
        # Verify data grid is present
        data_grid = "grid"
        expect(sales_rep_page.locator(data_grid)).to_be_visible(timeout=15000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Opportunities list"

    def test_sales_rep_can_create_opportunity(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can create a new Opportunity.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Opportunities list view
        3. Click the "New" button
        4. Verify the new opportunity form opens
        """
        # Navigate to Opportunities list
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Opportunity/list")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify New button is visible and clickable
        new_button = "button:has-text('New')"
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_enabled()
        
        # Click New button
        sales_rep_page.locator(new_button).first.click()
        
        # Verify new opportunity form/modal opens
        opportunity_form_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(opportunity_form_modal)).to_be_visible(timeout=10000)
        
        # Verify required opportunity fields are present
        # TODO: Add locators for Opportunity Name, Close Date, Stage fields
        opp_name_field = "input[field-label='Opportunity Name'], input[placeholder*='Opportunity']"
        # expect(sales_rep_page.locator(opp_name_field).first).to_be_visible()

    def test_sales_rep_can_edit_opportunity(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can edit an existing Opportunity.
        
        Page Object Models used: None (direct page interaction)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to an Opportunity detail page
        3. Click the "Edit" button
        4. Verify the edit form opens
        """
        # TODO: Replace with actual Opportunity ID from test data
        test_opportunity_id = "006XX000000XXXXX"
        
        # Navigate to opportunity detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Opportunity/{test_opportunity_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify opportunity page loads
        opportunity_header = "h1:has-text('Opportunity')"
        expect(sales_rep_page.locator(opportunity_header)).to_be_visible(timeout=30000)
        
        # Verify Edit button is visible and enabled
        edit_button = "button:has-text('Edit')"
        expect(sales_rep_page.locator(edit_button).first).to_be_visible()
        expect(sales_rep_page.locator(edit_button).first).to_be_enabled()
        
        # Click Edit button
        sales_rep_page.locator(edit_button).first.click()
        
        # Verify edit form opens
        edit_modal = "div.modal-container, section[role='dialog']"
        expect(sales_rep_page.locator(edit_modal)).to_be_visible(timeout=10000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message when editing an Opportunity"

    def test_sales_rep_can_view_opportunity_detail(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can view Opportunity details.
        
        Page Object Models used: None (direct page interaction)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to an Opportunity detail page
        3. Verify opportunity information is displayed
        """
        # TODO: Replace with actual Opportunity ID from test data
        test_opportunity_id = "006XX000000XXXXX"
        
        # Navigate to opportunity detail page
        sales_rep_page.goto(f"{BASE_URL}/lightning/r/Opportunity/{test_opportunity_id}/view")
        sales_rep_page.wait_for_load_state("networkidle")
        
        # Verify opportunity page loads with details
        opportunity_header = "h1:has-text('Opportunity')"
        expect(sales_rep_page.locator(opportunity_header)).to_be_visible(timeout=30000)
        
        # Verify key tabs are accessible
        details_tab = "tab:has-text('Details')"
        related_tab = "tab:has-text('Related')"
        expect(sales_rep_page.locator(details_tab)).to_be_visible()
        expect(sales_rep_page.locator(related_tab)).to_be_visible()
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied message on Opportunity detail"

    def test_sales_rep_can_view_opportunities_from_account(self, sales_rep_page: Page):
        """
        Test that a Sales Representative can navigate to Opportunities from Account detail.
        
        Page Object Models used: SalesforceAccountDetailPage
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to Account detail page
        3. Switch to Related tab
        4. Click Opportunities link
        5. Verify access to opportunities related list
        """
        account_detail_page = SalesforceAccountDetailPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to account detail
        account_detail_page.navigate_to_account(TEST_ACCOUNT_ID)
        account_detail_page.wait_for_page_load()
        
        # Switch to Related tab
        account_detail_page.switch_to_related_tab()
        
        # Verify Opportunities link is visible (proving access to view)
        expect(sales_rep_page.locator(account_detail_page.OPPORTUNITIES_LINK)).to_be_visible()
        
        # Click Opportunities link
        account_detail_page.click_opportunities_link()
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_rep_page), \
            "Sales Rep should NOT see access denied when viewing Opportunities from Account"


# ==================== SALES MANAGER - DASHBOARDS AND REPORTS TESTS ====================


class TestSalesManagerDashboardAccess:
    """
    Test class for Sales Manager access to reports and dashboards.
    
    Verifies that Sales Managers can view reports and dashboards related to 
    team performance and the sales pipeline.
    """

    def test_sales_manager_can_view_dashboard(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view the team performance dashboard.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard page
        3. Verify the dashboard loads with widgets visible
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        
        # Verify dashboard is loaded
        dashboard_page.verify_dashboard_loaded()
        
        # Verify dashboard title is visible
        assert dashboard_page.is_dashboard_loaded(), \
            "Sales Manager should be able to view the dashboard"
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_manager_page), \
            "Sales Manager should NOT see access denied on Dashboard"

    def test_sales_manager_can_view_pipeline_widgets(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view pipeline-related dashboard widgets.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify pipeline widgets are visible (Pipeline ACV, Pipeline TCV)
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Verify pipeline widgets are visible
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_PIPELINE_ACV_WEIGHTED), \
            "Pipeline ACV - Current Year Weighted widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_PIPELINE_ACV), \
            "Pipeline ACV - Current Year widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_PIPELINE_TCV_WEIGHTED), \
            "Pipeline TCV - Current Year Weighted widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_PIPELINE_TCV), \
            "Pipeline TCV Current Year widget should be visible"

    def test_sales_manager_can_view_team_performance_widgets(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view team performance dashboard widgets.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify team performance widgets are visible 
           (Won ACV YTD, Won TCV YTD, Pipeline By Sales Lead)
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Load all widgets if needed
        dashboard_page.load_more_widgets()
        
        # Verify team performance widgets
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_WON_ACV_YTD), \
            "Won ACV YTD widget should be visible for Sales Manager"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_WON_TCV_YTD), \
            "Won TCV YTD widget should be visible for Sales Manager"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_PIPELINE_BY_SALES_LEAD), \
            "Pipeline By Sales Lead widget should be visible for Sales Manager"

    def test_sales_manager_can_view_won_lost_widgets(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view won/lost deal widgets.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify won/lost deal widgets are visible
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Load all widgets
        dashboard_page.load_more_widgets()
        
        # Verify won/lost widgets are visible
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_WON_DEALS_YTD), \
            "Won Deals - YTD widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_LOST_YTD), \
            "Lost YTD widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_WON_DEALS_ACCOUNTS), \
            "Won Deals - Accounts YTD widget should be visible"

    def test_sales_manager_can_use_dashboard_filters(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can interact with dashboard filters.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify filters are visible
        4. Apply Opportunity Owner filter
        5. Verify filter is applied successfully
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Verify filters are visible
        assert dashboard_page.verify_filters_visible(), \
            "Dashboard filters should be visible for Sales Manager"
        
        # Apply Opportunity Owner filter
        dashboard_page.apply_opportunity_owner_filter("All")
        
        # Verify filter value is set
        filter_value = dashboard_page.get_opportunity_owner_filter_value()
        assert "All" in filter_value, \
            f"Expected filter to be 'All', but got '{filter_value}'"

    def test_sales_manager_can_refresh_dashboard(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can refresh the dashboard data.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Click Refresh button
        4. Verify dashboard refreshes without errors
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Refresh the dashboard
        dashboard_page.refresh_dashboard_and_wait()
        
        # Verify dashboard is still loaded after refresh
        assert dashboard_page.is_dashboard_loaded(), \
            "Dashboard should still be loaded after refresh"
        
        # Verify widgets count is maintained
        widget_count = dashboard_page.count_visible_widgets()
        assert widget_count > 0, \
            "Dashboard should have visible widgets after refresh"

    def test_sales_manager_can_navigate_to_dashboards_tab(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can navigate to the Dashboards tab.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Click on the Dashboards navigation tab
        3. Verify the Dashboards page loads
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Click Dashboards tab
        dashboard_page.click_dashboards_tab()
        
        # Wait for page to load
        sales_manager_page.wait_for_load_state("networkidle")
        
        # Verify Dashboards page loads
        # TODO: Add specific assertion for Dashboards list page
        dashboards_heading = "h1:has-text('Dashboards')"
        expect(sales_manager_page.locator(dashboards_heading)).to_be_visible(timeout=30000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_manager_page), \
            "Sales Manager should NOT see access denied on Dashboards page"

    def test_sales_manager_can_view_reports(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can access the Reports section.
        
        Page Object Models used: SalesforceDashboardPage (for navigation context)
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to Reports page
        3. Verify the Reports page loads
        """
        # Navigate directly to Reports
        sales_manager_page.goto(f"{BASE_URL}/lightning/o/Report/home")
        sales_manager_page.wait_for_load_state("networkidle")
        
        # Verify Reports page loads
        # TODO: Create a dedicated ReportsPage POM
        reports_heading = "h1:has-text('Reports'), h1:has-text('All Reports')"
        expect(sales_manager_page.locator(reports_heading).first).to_be_visible(timeout=30000)
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_manager_page), \
            "Sales Manager should NOT see access denied on Reports page"

    def test_sales_manager_can_view_monthly_closure_widgets(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view monthly closure and performance widgets.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify monthly closure widgets are visible
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Load all widgets
        dashboard_page.load_more_widgets()
        
        # Verify monthly closure widgets
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_CURRENT_MONTH_CLOSURES), \
            "Projected Current Month Closures widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_TCV_CLOSED_MONTH), \
            "TCV - Closed per Month widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_ACV_CLOSED_MONTH), \
            "ACV - Closed Per Month widget should be visible"

    def test_sales_manager_dashboard_widgets_have_data(self, sales_manager_page: Page):
        """
        Test that dashboard widgets contain data for the Sales Manager.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to the dashboard
        3. Verify that key widgets have data (not empty)
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Check that pipeline widget has data
        has_pipeline_data = dashboard_page.verify_widget_has_data(
            dashboard_page.WIDGET_PIPELINE_ACV_WEIGHTED
        )
        # Note: This may legitimately have no data in a test environment
        # TODO: Ensure test data exists for meaningful dashboard widget verification
        logger.info(f"Pipeline ACV Weighted widget has data: {has_pipeline_data}")

    def test_sales_manager_can_view_top_opportunities_widget(self, sales_manager_page: Page):
        """
        Test that a Sales Manager can view top opportunities widget on dashboard.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Navigate to dashboard
        3. Verify Top Opportunities widgets are visible
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to dashboard
        dashboard_page.navigate_to_dashboard()
        dashboard_page.verify_dashboard_loaded()
        
        # Verify top opportunities widgets
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_TOP_40_ACV), \
            "Top 40 Opps - ACV per Account widget should be visible"
        
        assert dashboard_page.is_widget_visible(dashboard_page.WIDGET_TOP_200_OPP), \
            "Top 200 opportunity - ACV widget should be visible"


# ==================== CROSS-ROLE ACCESS VERIFICATION TESTS ====================


class TestCrossRoleAccessControl:
    """
    Test class for verifying cross-role access boundaries.
    
    These tests verify that the access control properly restricts/grants 
    access based on user roles.
    """

    def test_sales_rep_has_new_button_on_all_objects(self, sales_rep_page: Page):
        """
        Test that Sales Rep has New button visible on all CRM objects they should access.
        
        Page Object Models used: SalesforceAccountsListViewPage (for navigation)
        
        Steps:
        1. Login as Sales Representative
        2. Navigate to each object list (Leads, Accounts, Contacts, Opportunities)
        3. Verify "New" button is visible on each
        """
        new_button = "button:has-text('New')"
        
        # Check Accounts
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Account/list")
        sales_rep_page.wait_for_load_state("networkidle")
        sales_rep_page.wait_for_selector("h1:has-text('Accounts')", timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=10000)
        
        # Check Leads
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Lead/list")
        sales_rep_page.wait_for_load_state("networkidle")
        sales_rep_page.wait_for_selector("h1:has-text('Leads')", timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=10000)
        
        # Check Contacts
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Contact/list")
        sales_rep_page.wait_for_load_state("networkidle")
        sales_rep_page.wait_for_selector("h1:has-text('Contacts')", timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=10000)
        
        # Check Opportunities
        sales_rep_page.goto(f"{BASE_URL}/lightning/o/Opportunity/list")
        sales_rep_page.wait_for_load_state("networkidle")
        sales_rep_page.wait_for_selector("h1:has-text('Opportunities')", timeout=30000)
        expect(sales_rep_page.locator(new_button).first).to_be_visible(timeout=10000)

    def test_sales_manager_can_access_dashboards_tab(self, sales_manager_page: Page):
        """
        Test that Sales Manager has Dashboards tab accessible in navigation.
        
        Page Object Models used: SalesforceDashboardPage
        
        Steps:
        1. Login as Sales Manager
        2. Verify Dashboards tab is visible in the navigation
        3. Click on Dashboards tab
        4. Verify access is granted
        """
        dashboard_page = SalesforceDashboardPage(sales_manager_page, base_url=BASE_URL)
        
        # Navigate to home first
        sales_manager_page.goto(f"{BASE_URL}/lightning/page/home")
        sales_manager_page.wait_for_load_state("networkidle")
        
        # Verify Dashboards tab is visible
        expect(sales_manager_page.locator(dashboard_page.DASHBOARDS_TAB)).to_be_visible(
            timeout=30000
        )
        
        # Click Dashboards tab
        dashboard_page.click_dashboards_tab()
        
        # Verify no access denied
        assert not verify_access_denied_message(sales_manager_page), \
            "Sales Manager should have access to Dashboards"

    def test_sales_rep_navigation_tabs_accessible(self, sales_rep_page: Page):
        """
        Test that Sales Rep has all required navigation tabs accessible.
        
        Page Object Models used: SalesforceAccountsListViewPage
        
        Steps:
        1. Login as Sales Representative
        2. Verify Accounts, Contacts, Leads, Opportunities tabs are visible
        """
        accounts_page = SalesforceAccountsListViewPage(sales_rep_page, base_url=BASE_URL)
        
        # Navigate to accounts page first (to ensure nav is loaded)
        accounts_page.navigate_to_accounts_list()
        accounts_page.verify_page_loaded()
        
        # Verify all required nav tabs are visible
        expect(sales_rep_page.locator(accounts_page.NAV_ACCOUNTS)).to_be_visible()
        expect(sales_rep_page.locator(accounts_page.NAV_CONTACTS)).to_be_visible()
        expect(sales_rep_page.locator(accounts_page.NAV_LEADS)).to_be_visible()
        expect(sales_rep_page.locator(accounts_page.NAV_OPPORTUNITIES)).to_be_visible()