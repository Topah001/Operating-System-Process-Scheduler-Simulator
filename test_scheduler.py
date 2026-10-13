import unittest
from scheduler import Process, fcfs, sjf, round_robin, averages

class SchedulerTests(unittest.TestCase):
    def setUp(self):
        self.jobs = [Process("A", 0, 5), Process("B", 1, 3), Process("C", 2, 1)]
    def test_fcfs_metrics(self):
        r = fcfs(self.jobs)
        self.assertEqual([(x.pid, x.waiting, x.turnaround) for x in r], [("A",0,5),("B",4,7),("C",6,7)])
        self.assertEqual(averages(r), {"average_waiting":10/3,"average_turnaround":19/3})
    def test_nonpreemptive_sjf(self):
        r = sjf(self.jobs)
        self.assertEqual([x.pid for x in r], ["A","C","B"])
        self.assertEqual([(x.waiting,x.turnaround) for x in r], [(0,5),(3,4),(5,8)])
    def test_round_robin(self):
        r = round_robin(self.jobs, 2)
        self.assertEqual([(x.pid,x.waiting,x.turnaround) for x in r], [("A",4,9),("B",4,7),("C",2,3)])
    def test_idle_gap_and_quantum(self):
        self.assertEqual(fcfs([Process("X",4,2)])[0].waiting, 0)
        with self.assertRaises(ValueError): round_robin(self.jobs, 0)
    def test_input_validation(self):
        for bad in ([], [Process("",0,1)], [Process("A",-1,1)], [Process("A",0,0)], [Process("A",0,1),Process("A",0,2)]):
            with self.subTest(bad=bad), self.assertRaises(ValueError): fcfs(bad)
        with self.assertRaises(ValueError): sjf([Process("A",1.5,2)])

if __name__ == "__main__": unittest.main()
