from hipercic.hipercore.authenticore.tests.auth_backends import BackendTest, RowlevelBackendTest, AnonymousUserBackendTest, NoAnonymousUserBackendTest, NoBackendsTest
from hipercic.hipercore.authenticore.tests.basic import BasicTestCase
from hipercic.hipercore.authenticore.tests.decorators import LoginRequiredTestCase
from hipercic.hipercore.authenticore.tests.forms import UserCreationFormTest, AuthenticationFormTest, SetPasswordFormTest, PasswordChangeFormTest, UserChangeFormTest, PasswordResetFormTest
from hipercic.hipercore.authenticore.tests.remote_user \
        import RemoteUserTest, RemoteUserNoCreateTest, RemoteUserCustomTest
from hipercic.hipercore.authenticore.tests.models import ProfileTestCase
from hipercic.hipercore.authenticore.tests.tokens import TokenGeneratorTest
from hipercic.hipercore.authenticore.tests.views \
        import PasswordResetTest, ChangePasswordTest, LoginTest, LogoutTest

# The password for the fixture data users is 'password'
