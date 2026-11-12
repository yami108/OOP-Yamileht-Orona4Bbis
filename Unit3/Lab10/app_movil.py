class SuscripcionExpiradaError(Exception):
    """Raised when attempting to execute restricted operations without an active membership."""
    pass


class PuntosInsuficientesError(Exception):
    """Raised when a transaction exceeds the available gem balance."""
    pass


class PerfilMovil:
    """Base class representing a standard mobile application user profile."""

    def __init__(
        self,
        username: str,
        gemas: int = 50,
        racha_dias: int = 1,
        notificaciones_activas: bool = True,
    ):
        if gemas < 0:
            raise ValueError("Initial gems cannot be negative.")
        self.username = username
        self.gemas = gemas
        self.racha_dias = racha_dias
        self.notificaciones_activas = notificaciones_activas

    def ganar_gemas(self, cantidad: int) -> int:
        """Increments the accumulated gem balance. Requires a strictly positive integer."""
        if cantidad <= 0:
            raise ValueError("The amount of gems to earn must be greater than zero.")
        self.gemas += cantidad
        return self.gemas

    def gastar_gemas(self, cantidad: int) -> int:
        """Decrements the gem balance after verifying positive value and sufficient funds."""
        if cantidad <= 0:
            raise ValueError("The amount of gems to spend must be greater than zero.")
        if cantidad > self.gemas:
            raise PuntosInsuficientesError(
                f"Insufficient gems. Available: {self.gemas}, Requested: {cantidad}."
            )
        self.gemas -= cantidad
        return self.gemas


class PerfilPro(PerfilMovil):
    """Derived subclass representing a Pro user profile with subscription benefits."""

    def __init__(
        self,
        username: str,
        meses_suscripcion: int,
        gemas: int = 50,
        racha_dias: int = 1,
        notificaciones_activas: bool = True,
    ):
        if meses_suscripcion <= 0:
            raise ValueError("Subscription period must be greater than zero.")
        super().__init__(username, gemas, racha_dias, notificaciones_activas)
        self.meses_suscripcion = meses_suscripcion
        self.es_pro = True

    def descargar_contenido_offline(self) -> str:
        """Evaluates subscription validity before allowing offline content download."""
        if self.meses_suscripcion <= 0:
            self.es_pro = False
            raise SuscripcionExpiradaError(
                "Pro subscription has expired. Offline download denied."
            )
        return f"Offline content downloaded successfully for {self.username}."