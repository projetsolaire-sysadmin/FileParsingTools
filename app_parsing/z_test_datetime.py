import datetime
import pandas as pd

df_passage_heure_ete = pd.date_range(start='30/10/2022 00:00:00', end='30/10/2022 05:00:00', freq="1H", name="m")
df_passage_heure_hiver = pd.date_range(start='27/03/2022 00:00:00', end='27/03/2022 05:00:00', freq="1H", name="m")
df3 = pd.date_range(start='26/05/2021 06:00:00', end='26/05/2021 10:00:00', freq="1H", name="m")
print(df_passage_heure_ete)
print(df_passage_heure_hiver)
print(pd.concat([df_passage_heure_ete, df_passage_heure_hiver], ignore_index=True))
