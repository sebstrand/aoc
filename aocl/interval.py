import math
from aocl.lib import visit


class Intervals:
    """Tracks integer intervals. Allows adding and removing intervals defined by start+end and
    allows iterating over the resulting merged (non-overlapping) intervals and/or the integers
    contained within them.

    >>> intervals = Intervals().add(0, 11).add(8, 20).remove(4, 4)
    >>> print(intervals)
    Intervals[(0, 3),(5, 20)]
    >>> len(intervals)
    20
    >>> intervals.size
    2
    >>> sum(intervals) == sum(range(0, 21)) - 4
    True
    """
    def __init__(self):
        self._intervals = []
        self._dirty = False

    @property
    def min(self):
        if len(self._intervals) == 0: return -math.inf

        self._clean()
        return self._intervals[0][0]

    @property
    def max(self):
        if len(self._intervals) == 0: return math.inf

        return max(end for _, end in self._intervals)

    @property
    def size(self):
        return len(self._intervals)

    @property
    def intervals(self):
        self._clean()
        return self._intervals

    def add(self, start, end):
        if end < start or end - start == math.inf: return

        self._intervals.append((start, end))
        self._dirty = True
        return self

    def remove(self, start, end):
        if end < self.min: return  # Nothing to do

        self._clean()
        intervals = []
        for i, interval in enumerate(self._intervals):
            old_start, old_end = interval
            if old_start > end:
                intervals += self._intervals[i:]
                break

            if start <= old_end and end >= old_start:
                # There is overlap
                if start <= old_start and end >= old_end:
                    continue
                elif start > old_start:
                    # Overlap at start or overlap inside
                    intervals.append((old_start, start - 1))
                    if end < old_end:
                        # Overlap inside, add new interval for end
                        intervals.append((end + 1, old_end))
                elif end < old_end:
                    # Overlap at end
                    intervals.append((end + 1, old_end))
            else:
                intervals.append(interval)

        self._intervals = intervals
        return self

    def _clean(self):
        if not self._dirty: return

        seen_x = -math.inf
        intervals = []
        for i, interval in enumerate(sorted(self._intervals)):
            x_start, x_end = interval
            if x_end > seen_x:
                if x_start <= seen_x:
                    x_start = seen_x + 1
                    if x_start <= x_end:
                        previous_interval = intervals[-1]
                        intervals[-1] = previous_interval[0], x_end
                else:
                    intervals.append(interval)
                seen_x = x_end

        self._intervals = intervals
        self._dirty = False

    def __iter__(self):
        self._clean()
        return visit(range(s, e+1) for s, e in self._intervals)

    def __len__(self):
        self._clean()
        return sum(r[1] - r[0] + 1 for r in self._intervals)

    def __str__(self):
        self._clean()
        return f'Intervals[{",".join([str(r) for r in self._intervals])}]'
