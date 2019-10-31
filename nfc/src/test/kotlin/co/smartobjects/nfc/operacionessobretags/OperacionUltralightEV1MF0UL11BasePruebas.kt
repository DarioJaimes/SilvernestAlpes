package co.smartobjects.nfc.operacionessobretags

import co.smartobjects.nfc.tags.mifare.ultralight.UltralightEV1
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import java.util.*
import kotlin.test.assertTrue


internal open class OperacionUltralightEV1MF0UL11BasePruebas : OperacionUltralightEV1BasePruebas()
{
    @BeforeEach
    open fun antesDeCadaTest()
    {
        operacionesCompuestas = obtenerOperacionesCompuestasParaUltralightEV1(UltralightEV1.VersionUltralightEV1.MF0UL11)
    }

    @Test
    fun dar_uid_ultralight_ev1_mf0ul11()
    {
        assertTrue(Arrays.equals(lector.uid, operacionesCompuestas.darUID()))
    }
}