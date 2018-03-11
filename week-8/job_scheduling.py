############################
#  WEEK 8: JOB SCHEDULING  #
############################

# PROBLEM 1
# The file jobs.txt describes a set of jobs with positive and integral weights and lengths. It has the format
#
# [number_of_jobs]
#
# [job_1_weight] [job_1_length]
#
# [job_2_weight] [job_2_length]
#
# ...
#
# For example, the third line of the file is "74 59", indicating that the second job has weight 74 and length 59.
#
# You should NOT assume that edge weights or lengths are distinct.
#
# Your task in this problem is to run the greedy algorithm that schedules jobs in decreasing order of the difference
# (weight - length). Recall from lecture that this algorithm is not always optimal. IMPORTANT: if two jobs have equal
# difference (weight - length), you should schedule the job with higher weight first. Beware: if you break ties in a
# different way, you are likely to get the wrong answer. You should report the sum of weighted completion times of the
# resulting schedule --- a positive integer --- in the box below.


def read_jobs():
    f = open('week-8/jobs.txt', mode='r')
    data = f.readlines()
    f.close()

    # num_jobs = int(data[0].strip())
    lines = data[1:]

    lengths = []
    weights = []

    for line in lines:
        length, weight = line.split()

        lengths.append(int(length))
        weights.append(int(weight))

    return list(zip(lengths, weights))


def schedule_by_difference(job_list):
    differences = list(map(lambda x: x[0] - x[1], job_list))
    # numbers = list(range(len(differences)))

    ordered_jobs = [job for (diff, job) in sorted(zip(differences, job_list))]

    return ordered_jobs


def sum_completion(job_list):
    sum_comp_time = 0

    comp_time = 0

    for (length, weight) in job_list:
        comp_time += length

        sum_comp_time += weight*comp_time

    return sum_comp_time


jobs = read_jobs()
jobs_diff = schedule_by_difference(jobs)

sum_diff = sum_completion(jobs_diff)

# The sum of the completion times ordered by the difference w-j - l_j is: 69,119,377,652
#   CHECK: CORRECT!
print(sum_diff)


# PROBLEM 2
# For this problem, use the same data set as in the previous problem.
#
# Your task now is to run the greedy algorithm that schedules jobs (optimally) in decreasing order of the ratio
# (weight/length). In this algorithm, it does not matter how you break ties. You should report the sum of weighted
# completion times of the resulting schedule --- a positive integer --- in the box below.


def schedule_by_ratio(job_list):
    ratios = list(map(lambda x: x[0]/x[1], job_list))
    # numbers = list(range(len(differences)))

    ordered_jobs = [job for (ratio, job) in sorted(zip(ratios, job_list))]

    return ordered_jobs

jobs_ratio = schedule_by_ratio(jobs)

sum_ratio = sum_completion(jobs_ratio)

# The sum of the completion times ordered by the ratio w_j/l_j is: 67,311,454,237
#   CHECK: CORRECT!
print(sum_ratio)

