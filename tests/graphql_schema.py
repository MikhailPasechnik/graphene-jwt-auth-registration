import graphene

from gjwt_auth.mutations import (
    Activate,
    DeleteAccount,
    Register,
    ResetPassword,
    ResetPasswordConfirm,
    )



class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    register = Register.Field()
    deleteAccount = DeleteAccount.Field()
    resetPassword = ResetPassword.Field()
    resetPasswordConfirm = ResetPasswordConfirm.Field()


schema = graphene.Schema(mutation=Mutation)
