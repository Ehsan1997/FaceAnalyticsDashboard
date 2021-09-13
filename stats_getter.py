import pickle

# stats_file = '../MultiStreamUnsupervisedFaceIdentification/stats.pkl'
# data = pickle.load(open(stats_file, 'rb'))
# most_recent_timestamp = max(data['time_to_person'].keys())
# print(data['time_to_person'][most_recent_timestamp].most_common(10))
# print(data['person_frequency'].most_common(10))
from os.path import getmtime


class StatsGetter:
    def __init__(self, stats_file):
        self.stats_file = stats_file
        self.data = pickle.load(open(self.stats_file, 'rb'))
        self.mtime = getmtime(self.stats_file)

    def update_data(self):
        new_mtime = getmtime(self.stats_file)
        if new_mtime != self.mtime:
            self.mtime = new_mtime
            self.data = pickle.load(open(self.stats_file, 'rb'))

    def get_recent_persons(self, n=10, id_only=True):
        '''
        :param n:
        :param id_only: Return IDs of the persons only instead of their frequency and ID.
        :return:
        '''
        most_recent_timestamp = max(self.data['time_to_person'].keys())
        if not id_only:
            return self.data['time_to_person'][most_recent_timestamp].most_common(n)
        return [i[0] for i in self.data['time_to_person'][most_recent_timestamp].most_common(n)]

    def get_frequent_persons(self, n=10, id_only=True):
        if not id_only:
            return self.data['person_frequency'].most_common(n)
        return [i[0] for i in self.data['person_frequency'].most_common(n)]

    def get_time_frequency_of_id(self, id):
        return self.data['person_to_time'][id].most_common()

if __name__ == '__main__':
    # stats_file = '../MultiStreamUnsupervisedFaceIdentification/stats.pkl'
    stats_file = '../MultiStreamUnsupervisedFaceIdentification/Dump/dunya/Stats/stats.pkl'
    stats_obj = StatsGetter(stats_file)
    print(stats_obj.get_time_frequency_of_id(0))