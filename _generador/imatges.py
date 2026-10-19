# Fotos de cada pàgina i parelles d'abans i després.
# Les parelles són del mateix lloc, comprovades mirant les fotos una a una.
# La carpeta equipos-materiales no s'hi fa servir: són una piscina, expositors
# d'una gelateria i peces de cotxe pintades, no feines d'aquests serveis.

PARELLES = {
    "bany": ("/slide-02-bany-abans.jpg", "/slide-02-bany-despres.jpg",
             "Bany: de banyera antiga a dutxa d’obra", "Baño: de bañera antigua a ducha de obra"),
    "terrassa": ("/slide-01-terrassa-abans.jpg", "/slide-01-terrassa-despres.jpg",
                 "Terrassa amb pèrgola i il·luminació", "Terraza con pérgola e iluminación"),
    "solars": ("/slide-06-solars-abans.jpg", "/slide-06-solars-despres.jpg",
               "Coberta amb plaques solars", "Cubierta con placas solares"),
    "garatge": ("/slide-04-garatge-abans.jpg", "/slide-04-garatge-despres.jpg",
                "Porta de garatge i llum exterior", "Puerta de garaje y luz exterior"),
    "garatge_int": ("/slide-05-garage-int-abans.jpg", "/slide-05-garage-int-despres.jpg",
                    "Garatge: instal·lació elèctrica, il·luminació i acabats", "Garaje: instalación eléctrica, iluminación y acabados"),
    "hum_terra": ("/humedades-reparaciones/reparacion-humedad-01.jpg", "/interiores-reformas/reforma-interior-04.jpg",
                  "Humitat a la part baixa de la paret, reparada", "Humedad en la parte baja de la pared, reparada"),
    "hum_habitacio": ("/humedades-reparaciones/reparacion-humedad-03.jpg", "/interiores-reformas/reforma-interior-17.jpg",
                      "Habitació amb humitat, reparada i pintada", "Dormitorio con humedad, reparado y pintado"),
    "hum_escala": ("/humedades-reparaciones/reparacion-humedad-02.jpg", "/interiores-reformas/reforma-interior-11.jpg",
                   "Escala: humitat a la paret i esglaons nous", "Escalera: humedad en la pared y peldaños nuevos"),
    "hum_volta": ("/humedades-reparaciones/reparacion-humedad-09.jpg", "/interiores-reformas/reforma-interior-16.jpg",
                  "Sostre de volta amb filtració, reparat", "Techo de bóveda con filtración, reparado"),
    "hum_escaleta": ("/interiores-reformas/reforma-interior-35.jpg", "/interiores-reformas/reforma-interior-34.jpg",
                     "Graó amb humitat, reparat", "Escalón con humedad, reparado"),
    "hum_rebedor": ("/interiores-reformas/reforma-interior-03.jpg", "/interiores-reformas/reforma-interior-01.jpg",
                    "Paret i sostre de l’escala, reparats i amb llum nova", "Pared y techo de la escalera, reparados y con luz nueva"),
    "hum_safareig": ("/humedades-reparaciones/reparacion-humedad-05.jpg", "/banos-lavaderos-fontaneria/bano-fontaneria-03.jpg",
                     "Safareig amb humitat, reparat", "Lavadero con humedad, reparado"),
    "furgo": ("/banos-lavaderos-fontaneria/bano-fontaneria-02.jpg", "/interiores-reformas/reforma-interior-19.jpg",
              "Interior de furgoneta fet a mida", "Interior de furgoneta hecho a medida"),
}

# id: (foto de capçalera, foto lateral o None, parelles)
FOTOS = {
    "reformes": ("/interiores-reformas/reforma-interior-15.jpg", "/interiores-reformas/reforma-interior-07.jpg", ["bany", "garatge_int", "hum_escala"]),
    "banys": ("/banos-lavaderos-fontaneria/bano-fontaneria-04.jpg", "/interiores-reformas/reforma-interior-21.jpg", ["bany"]),
    "cuines": ("/interiores-reformas/reforma-interior-15.jpg", "/interiores-reformas/reforma-interior-09.jpg", []),
    "fontaneria": ("/banos-lavaderos-fontaneria/bano-fontaneria-05.jpg", "/interiores-reformas/reforma-interior-07.jpg", ["bany", "hum_safareig"]),
    "electricitat": ("/slide-05-garage-int-despres.jpg", "/interiores-reformas/reforma-interior-01.jpg", ["garatge_int", "garatge"]),
    "aire": ("/interiores-reformas/reforma-interior-22.jpg", "/interiores-reformas/reforma-interior-29.jpg", []),
    "aerotermia": ("/slide-06-solars-despres.jpg", "/banos-lavaderos-fontaneria/bano-fontaneria-05.jpg", []),
    "plaques": ("/slide-06-solars-despres.jpg", None, ["solars"]),
    "pergoles": ("/hero-portada/hero-reformas-instalaciones-01.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-19.jpg", ["terrassa", "garatge"]),
    "fusteria": ("/terrazas-suelos-exteriores/terraza-suelo-exterior-04.jpg", "/interiores-reformas/reforma-interior-20.jpg", ["furgo"]),
    "humitats": ("/humedades-reparaciones/reparacion-humedad-12.jpg", None, ["hum_terra", "hum_habitacio", "hum_escala", "hum_volta", "hum_rebedor", "hum_escaleta", "hum_safareig"]),
    "manteniment": ("/hero-portada/hero-reformas-instalaciones-03.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-17.jpg", ["garatge", "hum_terra"]),
    "figueres": ("/interiores-reformas/reforma-interior-12.jpg", "/interiores-reformas/reforma-interior-07.jpg", []),
    "roses": ("/hero-portada/hero-reformas-instalaciones-05.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-13.jpg", []),
    "empuriabrava": ("/exteriores-fachadas-cerramientos/cerramiento-fachada-14.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-06.jpg", []),
    "cadaques": ("/exteriores-fachadas-cerramientos/cerramiento-fachada-02.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-21.jpg", []),
    "llanca": ("/hero-portada/hero-reformas-instalaciones-02.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-20.jpg", []),
    "lescala": ("/terrazas-suelos-exteriores/terraza-suelo-exterior-03.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-07.jpg", []),
    "castello": ("/hero-portada/hero-reformas-instalaciones-04.jpg", "/interiores-reformas/reforma-interior-14.jpg", []),
    "vilajuiga": ("/exteriores-fachadas-cerramientos/cerramiento-fachada-16.jpg", "/interiores-reformas/reforma-interior-23.jpg", []),
    "zona-nord": ("/hero-portada/hero-reformas-instalaciones-03.jpg", "/interiores-reformas/reforma-interior-15.jpg", ["bany", "terrassa"]),
    "zona-costa": ("/exteriores-fachadas-cerramientos/cerramiento-fachada-01.jpg", "/exteriores-fachadas-cerramientos/cerramiento-fachada-22.jpg", ["terrassa", "hum_terra"]),
}

# Text alternatiu de la foto lateral quan la foto ha canviat (ca, es).
# A les pàgines de municipi no es diu el poble: no sabem on es va fer cada foto.
ALTS = {
    "reformes": ("Bany reformat amb dutxa i moble suspès", "Baño reformado con ducha y mueble suspendido"),
    "cuines": ("Reforma interior en curs", "Reforma interior en curso"),
    "fontaneria": ("Bany renovat amb dutxa i moble suspès", "Baño renovado con ducha y mueble suspendido"),
    "electricitat": ("Escala reformada amb aplic de llum nou", "Escalera reformada con aplique de luz nuevo"),
    "aire": ("Dormitori reformat", "Dormitorio reformado"),
    "aerotermia": ("Equip d’aigua en un armari exterior", "Equipo de agua en un armario exterior"),
    "figueres": ("Bany reformat", "Baño reformado"),
    "roses": ("Pèrgola bioclimàtica en una casa de costa", "Pérgola bioclimática en una casa de costa"),
    "empuriabrava": ("Persiana i terrassa a tocar d’un canal", "Persiana y terraza junto a un canal"),
    "cadaques": ("Façana amb gelosia de fusta", "Fachada con celosía de madera"),
    "llanca": ("Tanca d’obra amb lames d’alumini", "Valla de obra con lamas de aluminio"),
    "lescala": ("Escala exterior en obra", "Escalera exterior en obra"),
    "castello": ("Escala exterior d’un habitatge", "Escalera exterior de una vivienda"),
    "vilajuiga": ("Llit alt de fusta fet a mida", "Cama alta de madera hecha a medida"),
    "zona-nord": ("Sala amb terra de fusta reformada", "Salón con suelo de madera reformado"),
    "zona-costa": ("Tarima de fusta en una terrassa", "Tarima de madera en una terraza"),
}
