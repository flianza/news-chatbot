select title,
    published,
    'A24' as source
from a24_items
union ALL
select title,
    published,
    'Caras' as source
from caras_items
union ALL
select title,
    published,
    'Exitoina' as source
from exitoina_items
union ALL
select title,
    published,
    'Google News' as source
from googlenews_items
union ALL
select title,
    published,
    'Minuto Uno' as source
from minutouno_items
union ALL
select title,
    published,
    'Primicias Ya' as source
from primiciasya_items
union ALL
select title,
    published,
    'Clarin' as source
from clarin_items