# Algobetting-Ekstraklasa
tu wszystko trzeba będzie jeszcze przeredagować

W tym projekcie:
\n 1.) Scrapuję dane z Ekstraklasy na oddsportal.org (historyczne dane bukmacherskie, sezony 12/13 - 24/25)
\n 2.) Scrapuję dane z Ekstraklasy na ekstrastats.pl (drużynowe dane z danych sezonów, sezony 14/15 - 23/24)
\n 3.) Procesuję dane z ekstrastats tak, aby można było je zmergować, dzielę je na gospodarze/goście, i łączę z danymi z oddsportala. Od razu je też normalizuję, tak aby można było je zastosować do dowolnego modelu
\n 4.) Dane z ekstrastats wkładam do drzewka decyzyjnego tak, aby z samego performance'u obu drużyn w poprzednim sezonie, i faktu że są gospodarzami/gośćmi w danym spotkaniu, spróbowało ono przewidzieć wynik spotkania. Jest to o tyle wygodna strategia, że nie wymaga aktualizacji danych na bieżąco - wystarczy to zrobić raz do roku, przed początkiem nwoego sezonu.
\n 5.) Wynik z drzewka decyzyjnego przekabacam przez historyczne oddsy i patrzę, co by się stało, gdyby ktoś faktycznie betował zgodnie z tym co model wypluje.

Wszystkie dane są w folderze data.zip, jeśli ktoś nie chce uruchamiać skryptów innych niż notebook z analizą, to wystarczy pobrać dane + notebooka.

oddsportal scraping.py samoczynnie scrapuje wszystko z tamtej strony. To znaczy, wystarczy wziąć skrypt, postawić prawidłowe PATH-y, poczekać 7-10 minut, i obudzimy się z jedną tabelą zawierającą wszystko czego można by chcieć.
Podobnie z ekstrastats scraping.py, ale tam parsowanie wymaga zmian w kodzie w zależności od sezonu. Kod zawarty w tym repo zwraca jedną tabelę, ale bez sezonów 14/15, 15/16, i 16/17. Dane w data.zip zawierają jednak dane i z tych sezonów, tak samo one też są poddane analizie.


yyy masturbancja
