import unittest
from datetime import timezone

from herramientas import podcasts

RSS = """<?xml version="1.0"?><rss xmlns:podcast="https://podcastindex.org/namespace/1.0"><channel><title>Demo</title>
<item><title>Why Treasuries Are Risky</title><pubDate>Mon, 05 Oct 2026 08:00:00 +0000</pubDate>
<description><![CDATA[<p>We talk <b>yields</b> &amp; the Fed.</p>]]></description><link>https://x/1</link>
<podcast:transcript url="https://t/1.srt?a=1&amp;b=2" type="application/srt"/><podcast:transcript url="https://t/1.txt" type="text/plain"/></item>
<item><title>Sin transcripcion</title><pubDate>Fri, 02 Oct 2026 08:00:00 -0000</pubDate><description>solo notas</description></item>
<item><title>Sin fecha valida</title><pubDate>ayer</pubDate></item>
</channel></rss>"""


class PruebasPodcasts(unittest.TestCase):
    def test_parsear_feed(self):
        eps = podcasts.parsear_feed(RSS)
        self.assertEqual(len(eps), 2)  # el que no tiene fecha valida se omite
        self.assertEqual(eps[0]["titulo"], "Why Treasuries Are Risky")
        self.assertEqual(eps[0]["fecha"].tzinfo, timezone.utc)
        self.assertEqual(eps[0]["descripcion"], "We talk yields & the Fed.")
        self.assertEqual(eps[0]["transcripciones"]["application/srt"], "https://t/1.srt?a=1&b=2")
        self.assertEqual(eps[1]["transcripciones"], {})

    def test_elegir_transcripcion_prefiere_texto(self):
        tipo, url = podcasts.elegir_transcripcion(podcasts.parsear_feed(RSS)[0]["transcripciones"])
        self.assertEqual((tipo, url), ("text/plain", "https://t/1.txt"))
        self.assertIsNone(podcasts.elegir_transcripcion({}))

    def test_texto_de_transcripcion(self):
        srt = "1\n00:00:00,000 --> 00:00:04,000\nHola Fed.\n\n2\n00:00:04,000 --> 00:00:06,000\nAdios.\n"
        self.assertEqual(podcasts.texto_de_transcripcion(srt), "Hola Fed. Adios.")
        self.assertEqual(podcasts.texto_de_transcripcion("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nOk"), "Ok")
        self.assertEqual(podcasts.texto_de_transcripcion("00:00:05\nSpeaker 1: texto"), "Speaker 1: texto")

    def test_palabras_clave_no_cuentan_subcadenas(self):
        r = podcasts.contar_palabras_clave("The Fed raised; the federal fund. Fed again. Bitcoin and ether, not whether.")
        self.assertEqual(r["Fed"], 2)
        self.assertEqual(r["bitcoin"], 1)
        self.assertEqual(r["ether"], 1)

    def test_siglas_sensibles_a_mayusculas(self):
        r = podcasts.contar_palabras_clave("She sat and was fed. The SAT and the Fed met; fed again.")
        self.assertEqual(r.get("SAT"), 1)
        self.assertEqual(r.get("Fed"), 1)


if __name__ == "__main__":
    unittest.main()
