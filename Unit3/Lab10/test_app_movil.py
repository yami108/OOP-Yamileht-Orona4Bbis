import pytest
from app_movil import (
    PerfilMovil,
    PerfilPro,
    PuntosInsuficientesError,
    SuscripcionExpiradaError,
)


# 1. State Isolation (@pytest.fixture)
@pytest.fixture
def perfil_estandar():
    """Provides a standardized instance of PerfilMovil for isolated tests."""
    return PerfilMovil(username="usuario_test")


# 2. Structural Integrity and Assertion Tests
def test_inicializacion_perfil_estandar(perfil_estandar):
    assert perfil_estandar.username == "usuario_test"
    assert perfil_estandar.gemas == 50
    assert perfil_estandar.racha_dias == 1
    assert perfil_estandar.notificaciones_activas is True


def test_inicializacion_gemas_negativas():
    with pytest.raises(ValueError):
        PerfilMovil(username="usuario_invalido", gemas=-10)


def test_gastar_gemas_valido(perfil_estandar):
    nuevo_saldo = perfil_estandar.gastar_gemas(20)
    assert nuevo_saldo == 30
    assert perfil_estandar.gemas == 30


# 3. Exception Validation (pytest.raises)
def test_gastar_gemas_insuficientes(perfil_estandar):
    with pytest.raises(PuntosInsuficientesError):
        perfil_estandar.gastar_gemas(100)


@pytest.mark.parametrize("cantidad_invalida", [0, -5, -100])
def test_gastar_gemas_cantidad_invalida(perfil_estandar, cantidad_invalida):
    with pytest.raises(ValueError):
        perfil_estandar.gastar_gemas(cantidad_invalida)


# 4. Parameterized Tests (@pytest.mark.parametrize)
@pytest.mark.parametrize(
    "cantidad, saldo_esperado",
    [
        (1, 51),
        (10, 60),
        (150, 200),
    ],
)
def test_ganar_gemas_valores_validos(perfil_estandar, cantidad, saldo_esperado):
    resultado = perfil_estandar.ganar_gemas(cantidad)
    assert resultado == saldo_esperado
    assert perfil_estandar.gemas == saldo_esperado


@pytest.mark.parametrize("cantidad_invalida", [0, -1, -50])
def test_ganar_gemas_valores_limite_invalidos(perfil_estandar, cantidad_invalida):
    with pytest.raises(ValueError):
        perfil_estandar.ganar_gemas(cantidad_invalida)


# 5. Type and Hierarchy Verification (isinstance) & PerfilPro Lifecycle
def test_jerarquia_y_ciclo_vida_perfil_pro():
    pro_user = PerfilPro(username="pro_gamer", meses_suscripcion=3)

    # Inheritance and attribute checks
    assert isinstance(pro_user, PerfilPro)
    assert isinstance(pro_user, PerfilMovil)
    assert pro_user.es_pro is True
    assert pro_user.meses_suscripcion == 3
    assert pro_user.gemas == 50

    # Valid offline download
    mensaje = pro_user.descargar_contenido_offline()
    assert "successfully" in mensaje

    # Simulate expiration of subscription months
    pro_user.meses_suscripcion = 0
    with pytest.raises(SuscripcionExpiradaError):
        pro_user.descargar_contenido_offline()

    # Verify state switched after expiration
    assert pro_user.es_pro is False


@pytest.mark.parametrize("meses_invalidos", [0, -1, -12])
def test_inicializacion_perfil_pro_invalida(meses_invalidos):
    with pytest.raises(ValueError):
        PerfilPro(username="pro_invalido", meses_suscripcion=meses_invalidos)