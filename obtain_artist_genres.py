import pickle
import csv
import spotipy
from functools import reduce


AUTH_TOKEN = ''


def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def main():
    # Init Spotipy client
    sp = spotipy.Spotify(auth=AUTH_TOKEN)

    all_results = dict()

    # Iterate through search results by year for each artist
    year_range = (1900, 2021)
    for year in range(*year_range):
        print(year)
        lim = 50
        for off in range(0, 2000, lim):
            search_res = sp.search(q=f'year:{year}', limit=lim, offset=off, type='artist', market='US')
            for res in search_res['artists']['items']:
                all_results[res['id']] = {
                    'name': res['name'],
                    'genres': res['genres'],
                }

    '''
    # Dump all_results to pickle object for re-usability
    with open('spotify_raw_data.pk1', 'wb') as fp:
        pickle.dump(all_results, fp, pickle.HIGHEST_PROTOCOL)

    with open('spotify_raw_data.pk1', 'rb') as fp:
        all_results = pickle.load(fp)
    '''

    # Write results to csv file
    with open('spotify_artist_genres.csv', 'w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=list(all_results.values())[0].keys())
        writer.writeheader()
        for res in all_results.values():
            writer.writerow(res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
