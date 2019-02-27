from flask import Blueprint

provider_blueprint = Blueprint("provider", __name__, url_prefix="/providers")


class ProviderViewSet:
    oh = "ohh"

    @provider_blueprint.route("/", methods=["GET"])
    def listing(self):
        return "Teste" + self.oh
