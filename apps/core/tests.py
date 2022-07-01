from django.test import TestCase

from apps.core.models import ReadingList, Book
from apps.accounts.models import User

class EmptySiteTestCase(TestCase):
    ############
    # EXAMPLE TESTS
    # Nothing to change in this class, it's only provided here for reference
    ############

    def test_homepage_shows_expected_links(self):
        # Ensures homepage has some expected text, and links to log-in and
        # sign-up
        response = self.client.get('/')
        self.assertContains(response, 'The Book Club')

        # "html=True" is a feature of Django that will tolerate slight
        # differences in HTML (e.g. whitespace, order of attributes)
        login_html = '<a class="nav-link" href="/account/login/">Log In</a>'
        self.assertContains(response, login_html, html=True)
        signup_html = '<a class="nav-link" href="/account/signup/">Sign up</a>'
        self.assertContains(response, signup_html, html=True)

    def test_results_indicates_empty(self):
        response = self.client.get('/')
        self.assertContains(response, 'No reading lists... yet!', html=True)

    def test_signup(self):
        # Simulate the POST request for a sign-up
        self.client.post('/account/signup/', {
            'username': 'testuser',
            'password1': 'g00d_p@55w0rd',
            'password2': 'g00d_p@55w0rd',
            'email': 'testuser@fake.com',
        })

        # Now make sure the account was created and shows expected HTML
        response = self.client.get('/')
        self.assertContains(response, 'Account created successfully. Welcome!', html=True)

        # Ensure the user is logged in & displaying a link to the user's page
        expected_navbar_link = 'href="/account/users/testuser/"'
        self.assertContains(response, expected_navbar_link)



class C3FunctionalFixtureTestCase(TestCase):

    #################
    ## CHALLENGE 3 ##
    #################

    # This is a feature of Django's testing framework that allows fixtures to
    # be loaded before each test, to allow test data in your tests
    fixtures = [
        'testing_data.json',
    ]

    def test_page_1_shows_expected_booklists(self):
        # This first test is to ensure the 4 expected book lists from the test
        # data are being displayed on the "first page"
        response = self.client.get('/')
        self.assertContains(response, 'My kids LOVE these books')
        self.assertContains(response, 'Dystopian YA')
        self.assertContains(response, 'Great American Novels')
        self.assertContains(response, 'Fantasy books I recently read')

    def test_page_1_shows_doesnt_show_page_2_books(self):
        # This test is to ensure that page 2 and page 3 titles do not show
        response = self.client.get('/')
        self.assertNotContains(response, '19th Century Classics')
        self.assertNotContains(response, 'The origins of science fiction')

    def test_page_2_shows_expected_4_books(self):
        response = self.client.get('/?page=2')
        # Challenge 3 TODO: Complete this for the 4 titles on Page 2

    def test_page_2_shows_doesnt_show_page_1_books(self):
        response = self.client.get('/?page=2')
        # Challenge 3 TODO: Complete this for a title on page 1 and Page 3




class C4SecurityTFDTestCase(TestCase):

    #################
    ## CHALLENGE 4 ##
    #################

    fixtures = [
        'testing_data.json',
    ]

    def test_list_deletion_security(self):
        # Log in as test user alicereader (who has password of "password")
        self.client.login(username='alicereader', password='password')

        # Check that list #8 is indeed created by someone else, and that there
        # are a total of 10 Reading Lists (as expected from the fixture)
        rl = ReadingList.objects.get(id=8)
        self.assertEqual(rl.creator_user.username, 'janeqhacker')
        total_count = ReadingList.objects.count()
        self.assertEqual(total_count, 10)

        # Now, simulate the deletion, and ensure that there are still 10
        self.client.post('/list/delete/8/')
        total_count = ReadingList.objects.count()
        # Challenge 4 TODO: Uncomment this line so the test can fail
        #self.assertEqual(total_count, 10)


    def test_book_deletion_security(self):
        # Log in as test user alicereader (who has password of "password")
        self.client.login(username='alicereader', password='password')

        # Check that book #44 is indeed created by someone else, and that there
        # are a total of 58 books (as expected from the fixture)
        b = Book.objects.get(id=44)
        self.assertEqual(b.reading_list.creator_user.username, 'janeqhacker')
        total_count = Book.objects.count()
        self.assertEqual(total_count, 58)

        self.client.post('/book-delete/44/')
        # Challenge 4 TODO: Finish this with the similar code to ensure there
        # are still 58 Books in the DB


class C5ModelReadingListUnitTestCase(TestCase):

    #################
    ## CHALLENGE 5 ##
    #################

    def setUp(self):
        # Setup is run before every test, and can be used to setup test data.
        # Since this is a "unit test", we won't be using fixtures since that
        # would be overkill -- "small" is the goal here.
        fake_user = User.objects.create_user('testuser')
        self.reading_list = ReadingList.objects.create(
            title='Testing list',
            category='fiction',
            creator_user=fake_user,
        )


    def test_increment_views(self):
        # Ensure the views start at 0
        self.assertEqual(self.reading_list.views, 0)
        self.reading_list.increment_views() # Run the method itself
        print('reading list views:', self.reading_list.views)
        # Challenge 5 TODO: Add an "assertEqual" to ensure the view count has
        # been incremented


    def test_recalculate_popularity(self):
        self.reading_list.views = 100
        self.reading_list.recalculate_popularity()
        # Challenge 5 TODO: Finish the unit test for recalculate_popularity
        # - with views at 100 (score should be 10)
        # - with views at 0   (score should be 0)

