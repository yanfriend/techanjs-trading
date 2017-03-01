from strategy.filters.basic_filter import BasicFilter


class HEFilter(BasicFilter):
    def filter(self):
        ret = super(HEFilter, self).filter()
        if not ret:
            return False

        ret = self.second_filter_cycle()  # not use it in online chat show, its too slow.
        if ret:
            reversed_index = [a[0] for a in ret]
            return self.second_filter_dry_up_volume(reversed_index)
        return ret

    def second_filter_cycle(self):
        """
        it has 5-6 cycle in half a year, each up 20%
        Focus on stocks that regularly exhibit 6 to 8 day cycles of 20% price movement
        :return:
        """
        index = 1
        cycle = 0
        ret = []

        while index < 128:  # half an year.
            if index >= len(self.df):
                print 'too short in {}'.format(self.symbol)
                return False
            highest = self.df.ix[-index]['High'].max()
            lowest = self.df.ix[-index-8:-index]['Low'].min()  # not include the last one.
            if highest/lowest > 1.2:  # 20%+ up
                cycle += 1
                low_date_index = self.df.ix[-index-8:-index]['Low'].idxmin()
                low_index = self.df.index.get_loc(low_date_index)  # number index, location actually

                index = len(self.df) - low_index  # move to the lowest bar.
                ret.append((index, low_date_index))
            else:
                index += 1 # move to next one
        if cycle >=5:
            # import ipdb; ipdb.set_trace()
            return ret
        else:
            return False

    def second_filter_dry_up_volume(self, reversed_index):
        """
        for each index, calculate five day low volume, include the index day.
        get average volume.
        if last volume < 1.5 * avg volume, then return True as in dry volume state; otherwise False.
        :param reversed_index:
        :return:
        """
        vol = 0
        count = 0
        for ind in reversed_index:
            vol += self.df.ix[-ind-4: -ind+1]['Volume'].min()  # [:-1] always not include the last one, but cant use 0
            count += 1
        avg_vol = vol*1.0/count
        return self.df.ix[-1]['Volume'] < 1.5 * avg_vol
