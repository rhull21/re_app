
# %% 
import pandas as pd
import matplotlib.pyplot as plt
# data (flows, event, day)
df_events = pd.DataFrame( { 'month' : ['June', 'July', 'August', 'September'],
                            'year'  : [2022, 2022, 2022, 2022],
                            'count(events)' : [3, 5, 6, 3], 
                            'count(dry_days)' :  [10, 22, 13, 15]
                            }
                            )

df_flow = pd.DataFrame( { 'month' : ['June', 'July', 'August', 'September'],
                            'year'  : [2022, 2022, 2022, 2022],
                            'flow' : [15, 23, 65, 19] } )

# plot as frequency 
fig, ax = plt.subplots(figsize=(6 ,6))
ax.bar(df_events['month'], df_events['count(events)'], zorder=0, alpha=0.5, color='blue', label='event count')
ax.set_ylabel('Number of Dry Events, Per Month')
ax2 = ax.twinx()
ax2.plot(df_flow['month'], df_flow['flow'], zorder=1, alpha=1, linewidth=3, color='red', label='flow')
ax2.set_ylabel('Flow in Cubic Feet Per Second, Daily Average Per Month')
ax.legend()
ax2.legend(loc=0)
plt.show()



# %%
