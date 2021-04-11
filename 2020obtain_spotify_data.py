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
    charset = ["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]

    # Iterate through search results by year for each track
    year_range = (2020, 2021)
    for year in range(*year_range):
        print(year)
        lim = 50
        for char in charset:
            print(char)
            for off in range(0, 2000, lim):
                search_res = sp.search(q=f'year:{year} track:"{char}"', limit=lim, offset=off, type='track', market='US')
                for res in search_res['tracks']['items']:
                    all_results[res['id']] = {
                        'id': res['id'],
                        'artists': reduce(lambda a, b: (a + ', ' if len(a) > 0 else a) + b['name'], res['artists'], ''),
                        'name': res['name'],
                        'popularity': res['popularity'],
                    }


    # Dump all_results to pickle object for re-usability
    with open('spotify_raw_data.pk1', 'wb') as fp:
        pickle.dump(all_results, fp, pickle.HIGHEST_PROTOCOL)

    with open('spotify_raw_data.pk1', 'rb') as fp:
        all_results = pickle.load(fp)


    counter = 0
    # Update results with audio features
    for ids in batch(list(all_results.keys()), 100):
        print(f'{counter}/{len(all_results)}')
        features_res = sp.audio_features(ids)
        for feat in features_res:
            if feat is not None:
                all_results[feat['id']].update(feat)
        counter += 100

    # Write results to csv file
    with open('2020spotify_results.csv', 'w', newline='', encoding='utf-8') as fp:
        writer = csv.DictWriter(fp, fieldnames=list(all_results.values())[0].keys())
        writer.writeheader()
        for res in all_results.values():
            writer.writerow(res)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()