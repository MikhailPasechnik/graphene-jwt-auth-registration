import graphene

from gjwt_auth.mutations import (
    Activate,
    DeleteAccount,
    Register,
    ResetPassword,
    ResetPasswordConfirm,
    )
from gjwt_auth.schema import User, Viewer


class RootQuery(graphene.ObjectType):
    viewer = graphene.Field(Viewer)

    def resolve_viewer(self, info, **kwargs):
        if info.context.user.is_authenticated:
            return info.context.user
        return None


class Mutation(graphene.ObjectType):
    activate = Activate.Field()
    register = Register.Field()
    deleteAccount = DeleteAccount.Field()
    resetPassword = ResetPassword.Field()
    resetPasswordConfirm = ResetPasswordConfirm.Field()


schema = graphene.Schema(query=RootQuery, mutation=Mutation)
