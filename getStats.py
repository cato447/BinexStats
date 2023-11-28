from urllib.request import urlopen
from bs4 import BeautifulSoup
from pytimeparse import parse
from matplotlib import pyplot as plt

url = "https://pwning.sec.in.tum.de/scoreboard/"

page = urlopen(url)

content = BeautifulSoup(page.read().decode(), 'html.parser')

teams = content.find_all("a", class_="link-underline link-underline-opacity-0 link-underline-opacity-100-hover", title=True)
names = [team.get_text() for team in teams]
times_with_points = [team['title'] for team in teams]
# convert times to hours
times = [parse(time_with_points.split('/')[0].strip()) / 3600 for time_with_points in times_with_points]
points = [int(time_with_points.split('/')[1].strip()) for time_with_points in times_with_points]
# filter out teams with no time entry
times = [time for time in times if time > 0]
points = points[0:len(times)]
names = names[0:len(times)]

fig, ax = plt.subplots()

ax.plot(names, times, 'o-', label='Binex Times')
ax.set_ylabel('Total time taken in hours')
ax.set_xlabel('Team name')
# Annotate each data point with its x-axis value
for x, y in zip(names, times):
    ax.annotate(f'{x}', (x, y), textcoords="offset points", xytext=(0,10), ha='center')

# Hide xticks
ax.set_xticks([])

ax.legend()

plt.show()

