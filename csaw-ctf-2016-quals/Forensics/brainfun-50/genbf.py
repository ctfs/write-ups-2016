text = 'flag{w3_r_th3_h0llow_m3n}'
nums = map(ord, text)
diffs = [nums[0]] + [b-a for a,b in zip(nums[:-1], nums[1:])]
print ''.join([('-' if x < 0 else '+')*abs(x)+'.' for x in diffs])
