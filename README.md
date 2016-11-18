Popis úkolu

Máte data o jednotlivých letech (segmentech) a batožinách. Vaším úkolem je nalézt
kombinace jednotlivých letů (itineráře, tzn. minimálně 2 segmenty) pro pasažéry
bez batožiny, jedním nebo dvěma kusy batožiny tak, aby segmenty navazovaly s časem
na přestup 1-4 hodiny. Jednotlivé sloupce jsou ve vstupních datech pojmenovány:

    source, destination vyjadřující kód letiště odletu a příletu
    departure, arrival jsou časy odletu a příletu
    price je cena za letenku bez batožiny
    bags_allowed je počet kusů batožiny které se daji dokoupit
    bag_price je cena za kus batožiny přikoupené navíc
    flight_number je unikátní identifikátor segmentu

Pro jednoduchou orientaci v nabídce nakombinovaných segmentů by bylo vhodné, aby
nabídky letů pro pasažéry s různým počtem batožiny již obsahovaly celkovou cenu 
za všechny segmenty včetně poplatků za batožinu.
Vstupní data (csv) (pouze ukázka)

(Data byla aktualizována viz. DostalJ kometář. Omlouváme se za chybu. Pokud vaše
řešení zavisí na původním formátu YYYY-DD-MM, budeme na to brát ohled)

source,destination,departure,arrival,flight_number,price,bags_allowed,bag_price
USM,HKT,2017-02-11T06:25:00,2017-02-11T07:25:00,PV404,24,1,9
USM,HKT,2017-02-12T12:15:00,2017-02-12T13:15:00,PV755,23,2,9

Výstup

    Výstupní data můžou být v jakémkoliv formátu vhodném k dalšímu zpracování.
    Ignorovat opakování segmentů (A->B) v kombinaci. A a B představují kód letiště.
        A->B->A->B je nevalidní kombinace.
        A->B->A je validní kombinace.

Zpracování

    Úkol byl navržený tak, aby začátečníkům poskytl výzvu a možnost vyzkoušet si
    základní datové typy a kontrolní struktury (if, for atd.), a zdatnějším lidem
    kteří už dříve programovali v jiném jazyce trvalo zpracování chvilku.
    Řešení by mělo být jednoduché
    Neočekáváme, že řešení bude optimalizované na výpočetní náročnost nebo
    využití paměti (pokud vás to však baví a chcete využít matematické znalosti
    ze školy, můžete)

Použití

Vstupní data bude program číst ze stdin a bude jej tak možné spustit následujícím
způsobem cat input.csv | find_combinations.py skript poté zapíše výstup na stdout
a případné chyby na stderr.
