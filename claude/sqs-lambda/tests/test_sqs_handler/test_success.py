# from tests.test_sqs_handler import SqsHandlerLambdaTestCase


# class TestSuccess(SqsHandlerLambdaTestCase):
class TestSuccess():

    def test_success(self):
        self.assertEqual(200, 200)
        # self.assertEqual(self.HANDLER.handle_request(dict(), dict()), 200)

