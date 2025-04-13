from typing import List
class Solution(object):        
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        ans = []
        twoNumMap = {}
        n = len(nums)

        for i in range(n):
            inum = nums[i]
            if inum in twoNumMap:
                for pair in twoNumMap[inum]:
                    lst = sorted([pair[0], pair[1], inum])
                    if lst not in ans:
                        ans.append(lst)
            for j in range(i):
                compliment = 0 - nums[i] - nums[j]
                pair = tuple(sorted([nums[j],nums[i]]))
                if compliment in twoNumMap:
                    if pair not in twoNumMap[compliment]:
                        twoNumMap[compliment].append(pair)
                else: 
                    twoNumMap[compliment] = [(nums[j],nums[i])]

        return ans
    
    def threeSumAns(self, nums: List[int]) -> List[List[int]]:

        res = set()

        #1. Split nums into three lists: negative numbers, positive numbers, and zeros
        n, p, z = [], [], []
        for num in nums:
            if num > 0:
                p.append(num)
            elif num < 0: 
                n.append(num)
            else:
                z.append(num)

        #2. Create a separate set for negatives and positives for O(1) look-up times
        N, P = set(n), set(p)

        #3. If there is at least 1 zero in the list, add all cases where -num exists in N and num exists in P
        #   i.e. (-3, 0, 3) = 0
        if z:
            for num in P:
                if -1*num in N:
                    res.add((-1*num, 0, num))

        #3. If there are at least 3 zeros in the list then also include (0, 0, 0) = 0
        if len(z) >= 3:
            res.add((0,0,0))

        #4. For all pairs of negative numbers (-3, -1), check to see if their complement (4)
        #   exists in the positive number set
        for i in range(len(n)):
            for j in range(i+1,len(n)):
                target = -1*(n[i]+n[j])
                if target in P:
                    res.add(tuple(sorted([n[i],n[j],target])))

        #5. For all pairs of positive numbers (1, 1), check to see if their complement (-2)
        #   exists in the negative number set
        for i in range(len(p)):
            for j in range(i+1,len(p)):
                target = -1*(p[i]+p[j])
                if target in N:
                    res.add(tuple(sorted([p[i],p[j],target])))

        return res