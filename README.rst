makstat
=======

Пакет за работа со отворени податоци во Македонија

Завод за статистика
-------------------

Податоците може да се најдат `овде <http://makstat.stat.gov.mk/pxweb2007bazi/Database/StatistikaPoOblasti/databasetree.asp>`_. Форматот ``.px`` е затворен (proprietery).

Со скриптата ``px2json`` овие фајлови може да се парсираат и при што излезот е во ``json`` формат. На пример: ::

  python px2json.py < Grad_Reg_OdobrGradbaBrojInvestitor_mk.px

Со скриптата ``px2h5`` излезот е во ``HDF5`` формат. На пример: ::

  python px2json.py < Grad_Reg_OdobrGradbaBrojInvestitor_mk.px > gradbi.h5


Пример за користење на API: ::

    from makstat.zavod import iter_contextual_atom_data
    with open('some_file.px', 'r') as f:
        all_data = f.read().decode('cp1251').split('\r\n')
    for data in iter_contextual_atom_data(all_data):
        . . .

