# -*- coding: utf-8 -*
import unittest

from tests.FlaskClientBaseTestCase import FlaskClientBaseTestCase
from tests.errorDefinitions.errorConstants import PERSON_ACCESS_DOES_NOT_EXISTS_CODE
from tests.testCommons.testClients.testClientViewTestCase import CLIENT_ENTITY_NAME, create_test_client
from tests.testCommons.testLocations.testUbicacionViewTestCase import create_test_location, LOCATION_ENTITY_NAME
from tests.testsCJM.testOrders import LOCATION_ID_NAME, \
    RESERVATION_ID_NAME, PERSON_RESERVATION_ID_NAME, ACCESSES_NAME, ACCESS_TIME_NAME, \
    OK_OVERFLOW_STATE, OVERFLOWN_OVERFLOW_STATE, TEMPORALLY_OVERFLOWN_OVERFLOW_STATE, get_and_check_available_funds_for_access, \
    get_and_check_parent_balance_for_access, get_and_check_balance_for_access
from tests.testsCJM.testPaquetes.testPaqueteViewTestCase import create_test_package
from tests.testsCJM.testPersons.testPersonaViewTestCase import create_test_person, PERSON_ENTITY_NAME
from tests.testsCJM.testReservas.testAccessTopoffsViewTestCase import create_test_access_topoff
from tests.testsCJM.testReservas.testReservaPersonaViewTestCase import create_test_person_reservation, \
    PERSON_RESERVATION_ENTITY_NAME, change_person_reservation_active_status
from tests.testsCJM.testReservas.testReservaViewTestCase import RESERVATION_ENTITY_NAME, create_test_reservation


class PersonAccessesForPackageWithAccessTopoffsViewTestCase(FlaskClientBaseTestCase):
    ID_NAME = u"id"

    ENTITY_DOES_NOT_EXISTS_CODE = PERSON_ACCESS_DOES_NOT_EXISTS_CODE
    RESOURCE_URL = u"/clients/{0}/person-accesses/"
    SPECIFIC_RESOURCE_BASE_URL = u"/clients/{0}/reservations/{1}/persons-reservations/{2}/person-accesses/"

    ATTRIBUTES_NAMES_BY_FIELDS = {LOCATION_ID_NAME: "TEST_PERSON_ACCESS_ID_LOCATION",
                                  ACCESSES_NAME: "TEST_PERSON_ACCESS_ACCESSES"}

    NUMBER_OF_ENTITIES = 1
    ENTITY_NAME = 'person-access-order'

    TEST_CLIENT_NAME = "Test client"
    TEST_CLIENT_REQUIRES_LOGIN = True

    TEST_USER_USERNAME = "test_user"
    TEST_USER_PASSWORD = "test_password"
    TEST_USER_ROLE = None

    TEST_PACKAGE_NAME = "Test package"
    TEST_PACKAGE_PRICE = 100.5
    TEST_PACKAGE_DESCRIPTION = "Test description"
    TEST_PACKAGE_VALID_FROM = "19900101010101"
    TEST_PACKAGE_VALID_THROUGH = "21000101010101"
    TEST_PACKAGE_DURATION = 5
    TEST_PACKAGE_ID_SOCIAL_EVENT = None

    NUMBER_LOCATIONS = 5
    TEST_LOCATION_TYPE = "CITY"
    TEST_LOCATION_NAME = "Test location"
    TEST_LOCATION_PARENT_LOCATION_ID = None

    TEST_PERSON_NAME = "Test person"
    TEST_PERSON_DOCUMENT_TYPE = "CC"
    TEST_PERSON_DOCUMENT_NUMBER = "12345"
    TEST_PERSON_MAIL = "mail@test.com"
    TEST_PERSON_GENDER = "m"
    TEST_PERSON_BIRTHDATE = "19900101"
    TEST_PERSON_TYPE = "Adulto"
    TEST_PERSON_CATEGORY = "A"
    TEST_PERSON_AFFILIATION = "Cotizante"
    TEST_PERSON_NATIONALITY = "Colombiano"
    TEST_PERSON_PROFESSION = "Ingeniero"
    TEST_PERSON_CITY_OF_RESIDENCE = "Bogotá"
    TEST_PERSON_COMPANY = "Empresa"

    TEST_SKU_CATEGORY_NAME = "Test Category"
    TEST_SKU_CATEGORY_PARENT_SKU_CATEGORY_ID = None

    TEST_SKU_NAME = "Test SKU"
    TEST_SKU_MEASURE_UNIT = "Unidad"
    TEST_SKU_COST = 100.5
    TEST_SKU_EAN_CODE = None

    TEST_PERSON_RESERVATION_ID_RESERVATION = None
    TEST_PERSON_RESERVATION_PAYMENT = TEST_PACKAGE_PRICE
    TEST_PERSON_RESERVATION_INITIAL_DATE = "20100101010101"
    TEST_PERSON_RESERVATION_FINAL_DATE = TEST_PERSON_RESERVATION_INITIAL_DATE

    TEST_RESERVATION_COMPANY = "Test company"
    TEST_RESERVATION_PAYMENT = TEST_PACKAGE_PRICE * 50
    TEST_RESERVATION_INITIAL_DATE = TEST_PERSON_RESERVATION_INITIAL_DATE
    TEST_RESERVATION_FINAL_DATE = TEST_PERSON_RESERVATION_INITIAL_DATE

    TEST_ACCESS_TOPOFF_TRANSACTION_NUMBER = "123456"
    TEST_ACCESS_TOPOFF_TOPOFF_TIME = "20100101010101"

    UNLIMITED_AMOUNT_NAME = u"unlimited-amount"

    def _create_package_location(self):
        create_test_location(self, create_new_location=True)
        self.TEST_PACKAGE_ID_LOCATION = self.expected_ids[LOCATION_ENTITY_NAME]

    def create_access_topoff(self):
        create_test_location(self, create_new_location=True)
        self.TEST_ACCESS_TOPOFF_ID_LOCATION = self.expected_ids[LOCATION_ENTITY_NAME]
        total_consumptions = self.NUMBER_OF_ENTITIES * self.number_of_accesses
        self.TEST_ACCESS_TOPOFF_AMOUNT = total_consumptions
        create_test_access_topoff(self, create_new_topoff=True)

    def create_package_with_restricted_consumption(self):
        self._create_package_location()
        self.TEST_PACKAGE_RESTRICTED_CONSUMPTION = True
        create_test_package(self, create_new_package=True)

    def create_package_without_restricted_consumption(self):
        self._create_package_location()
        self.TEST_PACKAGE_RESTRICTED_CONSUMPTION = False
        create_test_package(self, create_new_package=True)

    def create_person_reservation_for_last_package(self, activate_package=True):
        create_test_reservation(self)

        create_test_person(self, create_new_person=True)
        self.TEST_PERSON_RESERVATION_ID_PERSON = self.expected_ids[PERSON_ENTITY_NAME]

        create_test_person_reservation(self, create_new_person_reservation=True)
        if activate_package:
            change_person_reservation_active_status(self, self.expected_ids[PERSON_RESERVATION_ENTITY_NAME], True)

    def create_package_with_restricted_consumption_and_person_reservation(self):
        self.create_package_with_restricted_consumption()
        self.create_person_reservation_for_last_package()
        self.create_access_topoff()

    def create_package_without_restricted_consumption_and_person_reservation(self):
        self.create_package_without_restricted_consumption()
        self.create_person_reservation_for_last_package()
        self.create_access_topoff()

    def create_test_accesses(self):
        accesses = []
        for access_number in range(self.number_of_accesses):
            if self.access_time_template is None:
                access_time = None
            else:
                access_time = self.access_time_template.format(access_number)
            access = {RESERVATION_ID_NAME: self.expected_ids[RESERVATION_ENTITY_NAME],
                      PERSON_RESERVATION_ID_NAME: self.expected_ids[PERSON_RESERVATION_ENTITY_NAME],
                      ACCESS_TIME_NAME: access_time}
            accesses.append(access)
        return accesses

    def create_and_assign_accesses(self):
        accesses = self.create_test_accesses()
        self.assign_field_value(ACCESSES_NAME, accesses)
        self.assign_field_value(LOCATION_ID_NAME, self.expected_ids[LOCATION_ENTITY_NAME])

    def setUp(self):
        super(PersonAccessesForPackageWithAccessTopoffsViewTestCase, self).setUp()
        create_test_client(self)

        self.number_of_accesses = 1
        self.access_time_template = "2010010102010{0}"
        self.is_unlimited = False
        self.expected_state = OK_OVERFLOW_STATE

    @classmethod
    def parse_values_to_default_format(cls, request_values, entity_number, is_create):
        accesses = request_values.get(ACCESSES_NAME)
        for access in accesses:
            access[LOCATION_ID_NAME] = request_values.get(LOCATION_ID_NAME)
        return accesses

    @classmethod
    def get_ancestor_entities_names(cls):
        return [CLIENT_ENTITY_NAME]

    @classmethod
    def get_ancestor_entities_names_for_specific_resource(cls):
        return [CLIENT_ENTITY_NAME, RESERVATION_ENTITY_NAME, PERSON_RESERVATION_ENTITY_NAME]

    def test_check_available_funds_and_balance_for_new_reservation(self):
        self.create_package_with_restricted_consumption_and_person_reservation()
        self.expected_amount = self.TEST_ACCESS_TOPOFF_AMOUNT
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_new_reservation_with_multiple_days(self):
        self.TEST_PERSON_RESERVATION_INITIAL_DATE = "20100101010101"
        self.TEST_RESERVATION_INITIAL_DATE = "20100101010101"
        self.TEST_PERSON_RESERVATION_FINAL_DATE = "20100103010101"
        self.TEST_RESERVATION_FINAL_DATE = "20100103010101"

        self.create_package_with_restricted_consumption_and_person_reservation()
        self.expected_amount = self.TEST_ACCESS_TOPOFF_AMOUNT
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_new_reservation_and_unlimited_access(self):
        self.number_of_accesses = 0
        self.create_package_with_restricted_consumption_and_person_reservation()
        self.expected_amount = 0
        self.is_unlimited = True
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_full_reservation(self):
        self.create_package_with_restricted_consumption_and_person_reservation()
        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_full_reservation_consuming_child_location(self):
        self.create_package_with_restricted_consumption_and_person_reservation()
        self.TEST_LOCATION_PARENT_LOCATION_ID = self.expected_ids[LOCATION_ENTITY_NAME]
        self.TEST_LOCATION_TYPE = "ZONE"
        create_test_location(self, create_new_location=True)

        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

        self.expected_ids[LOCATION_ENTITY_NAME] = self.TEST_LOCATION_PARENT_LOCATION_ID
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_overflown_reservation_consuming_child_location(self):
        self.create_package_with_restricted_consumption_and_person_reservation()
        self.TEST_LOCATION_PARENT_LOCATION_ID = self.expected_ids[LOCATION_ENTITY_NAME]
        self.TEST_LOCATION_TYPE = "ZONE"
        create_test_location(self, create_new_location=True)

        self.create_and_assign_accesses()
        self.do_create_requests()
        self.access_time_template = "2010010101020{0}"
        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        self.expected_state = OVERFLOWN_OVERFLOW_STATE
        get_and_check_available_funds_for_access(self)
        self.expected_amount = -self.TEST_ACCESS_TOPOFF_AMOUNT
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

        self.expected_ids[LOCATION_ENTITY_NAME] = self.TEST_LOCATION_PARENT_LOCATION_ID
        self.expected_amount = 0
        self.expected_state = OK_OVERFLOW_STATE
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_reservation_with_person_accesses_and_unlimited_access(self):
        self.number_of_accesses = 0
        self.create_package_with_restricted_consumption_and_person_reservation()

        self.number_of_accesses = 1
        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        self.is_unlimited = True
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_reservation_with_excess_person_accesses(self):
        self.create_package_with_restricted_consumption_and_person_reservation()

        self.create_and_assign_accesses()
        self.do_create_requests()
        self.access_time_template = "2010010101020{0}"
        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        self.expected_state = OVERFLOWN_OVERFLOW_STATE
        get_and_check_available_funds_for_access(self)
        self.expected_amount = -self.TEST_ACCESS_TOPOFF_AMOUNT
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_previously_full_reservation_after_delete(self):
        self.create_package_with_restricted_consumption_and_person_reservation()

        self.create_and_assign_accesses()
        self.do_create_requests()
        self.do_delete_requests()
        self.expected_amount = self.TEST_ACCESS_TOPOFF_AMOUNT
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)

    def test_check_available_funds_and_balance_for_full_reservation_with_topoffs_after_accesses(self):
        self.TEST_ACCESS_TOPOFF_TOPOFF_TIME = "20100101230101"
        self.create_package_with_restricted_consumption_and_person_reservation()

        self.create_and_assign_accesses()
        self.do_create_requests()
        self.expected_amount = 0
        self.expected_state = TEMPORALLY_OVERFLOWN_OVERFLOW_STATE
        get_and_check_available_funds_for_access(self)
        get_and_check_balance_for_access(self)
        get_and_check_parent_balance_for_access(self)
        
if __name__ == '__main__':
    unittest.main()