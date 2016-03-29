with recursive
str(str)as(select cast(substr(group_concat(name,''),:OFFSET,:LENGTH)as blob)from procedures order by id),
K(K)as(values(cast('36140903603905402710 606105819325044196641185483991200080426282173595542492613131770035416233655287942949252332304563134180460368242546261952792965006123653532941291707863225465664 64371771339210699943593408605  3801608336344889613889429448 568446438327516360641076033351163531501285028582942435635121735328473236835956242945887382272392833183903056242596577402763975236127289335341394696643200236656 68127917439364300743572445317  7602918936546028093873151461 530742520329962864540963364521126891415287861239142375332411700485571239998069042939157732240044497187331335942643555522734768916130915164941494442263174756917 7187872593951481745' as blob))),
s(s)as(values(cast(' 7121722 7121722 7121722 7121722 5 91420 5 91420 5 91420 5 91420 4111623 4111623 4111623 4111623 6101521 6101521 6101521 6101521' as blob))),
g(g)as(values(cast(' 0 1 2 3 4 5 6 7 8 9101112131415 1 611 0 51015 4 914 3 813 2 712 5 81114 1 4 71013 0 3 6 91215 2 0 714 512 310 1 815 613 411 2 9' as blob))),
md5(state,i,off,m,lra,ns,a0,b0,c0,d0,a,b,c,d)as(values(0,0,1,null,null,null,:A0,:B0,:C0,:D0,0,0,0,0)union all
	select
		(state+1)%129,
		case when state>=2 and state&1=0 then (i+1)&63 else i end,
		case when state=128 then off+64 else off end,

		case when state=0 then
			printf('%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d%10d',
				(unicode(substr(str,off+3,1))<<24)|(unicode(substr(str,off+2,1))<<16)|(unicode(substr(str,off+1,1))<<8)|unicode(substr(str,off+0,1)),
				(unicode(substr(str,off+7,1))<<24)|(unicode(substr(str,off+6,1))<<16)|(unicode(substr(str,off+5,1))<<8)|unicode(substr(str,off+4,1)),
				(unicode(substr(str,off+11,1))<<24)|(unicode(substr(str,off+10,1))<<16)|(unicode(substr(str,off+9,1))<<8)|unicode(substr(str,off+8,1)),
				(unicode(substr(str,off+15,1))<<24)|(unicode(substr(str,off+14,1))<<16)|(unicode(substr(str,off+13,1))<<8)|unicode(substr(str,off+12,1)),
				(unicode(substr(str,off+19,1))<<24)|(unicode(substr(str,off+18,1))<<16)|(unicode(substr(str,off+17,1))<<8)|unicode(substr(str,off+16,1)),
				(unicode(substr(str,off+23,1))<<24)|(unicode(substr(str,off+22,1))<<16)|(unicode(substr(str,off+21,1))<<8)|unicode(substr(str,off+20,1)),
				(unicode(substr(str,off+27,1))<<24)|(unicode(substr(str,off+26,1))<<16)|(unicode(substr(str,off+25,1))<<8)|unicode(substr(str,off+24,1)),
				(unicode(substr(str,off+31,1))<<24)|(unicode(substr(str,off+30,1))<<16)|(unicode(substr(str,off+29,1))<<8)|unicode(substr(str,off+28,1)),
				(unicode(substr(str,off+35,1))<<24)|(unicode(substr(str,off+34,1))<<16)|(unicode(substr(str,off+33,1))<<8)|unicode(substr(str,off+32,1)),
				(unicode(substr(str,off+39,1))<<24)|(unicode(substr(str,off+38,1))<<16)|(unicode(substr(str,off+37,1))<<8)|unicode(substr(str,off+36,1)),
				(unicode(substr(str,off+43,1))<<24)|(unicode(substr(str,off+42,1))<<16)|(unicode(substr(str,off+41,1))<<8)|unicode(substr(str,off+40,1)),
				(unicode(substr(str,off+47,1))<<24)|(unicode(substr(str,off+46,1))<<16)|(unicode(substr(str,off+45,1))<<8)|unicode(substr(str,off+44,1)),
				(unicode(substr(str,off+51,1))<<24)|(unicode(substr(str,off+50,1))<<16)|(unicode(substr(str,off+49,1))<<8)|unicode(substr(str,off+48,1)),
				(unicode(substr(str,off+55,1))<<24)|(unicode(substr(str,off+54,1))<<16)|(unicode(substr(str,off+53,1))<<8)|unicode(substr(str,off+52,1)),
				(unicode(substr(str,off+59,1))<<24)|(unicode(substr(str,off+58,1))<<16)|(unicode(substr(str,off+57,1))<<8)|unicode(substr(str,off+56,1)),
				(unicode(substr(str,off+63,1))<<24)|(unicode(substr(str,off+62,1))<<16)|(unicode(substr(str,off+61,1))<<8)|unicode(substr(str,off+60,1))
			)
		else m end,

		case when state&1=0 then lra else
			a
				+cast(substr(K,i*10+1,10)as integer)
				+cast(substr(m,cast(substr(g,i*2+1,2)as integer)*10+1,10)as integer)
				+case
					when i<=15 then (b&c)|(~b&d)
					when i<=31 then (d&b)|(~d&c)
					when i<=47 then (~b&c&~d)|(~b&~c&d)|(b&~c&~d)|(b&c&d)
					when i<=63 then (~c&(b|~d))|(c&~(b|~d))
				end
		end&0xffffffff,

		case when state&1=0 then ns else cast(substr(s,i*2+1,2)as integer) end,

		case when state=0 then (a0+a)&0xffffffff else a0 end,
		case when state=0 then (b0+b)&0xffffffff else b0 end,
		case when state=0 then (c0+c)&0xffffffff else c0 end,
		case when state=0 then (d0+d)&0xffffffff else d0 end,

		case
			when state=0 then (a0+a)&0xffffffff
			when state&1=0 then d
			else a end,
		case
			when state=0 then (b0+b)&0xffffffff
			when state&1=0 then (b+(((lra<<ns)&0xffffffff)|(lra>>(32-ns))))&0xffffffff
			else b end,
		case
			when state=0 then (c0+c)&0xffffffff
			when state&1=0 then b
			else c end,
		case
			when state=0 then (d0+d)&0xffffffff
			when state&1=0 then c
			else d end
	from md5,str,K,s,g where off<=:LENGTH or state=0)
select printf('%08x%08x%08x%08x',a0,b0,c0,d0)from md5 where off>:LENGTH and state=1