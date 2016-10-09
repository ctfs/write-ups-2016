#!/usr/bin/env ruby

# {{{ === requires ===
require 'digest'
require 'json'
require 'openssl'
require 'securerandom'
require 'timeout'
# }}}

Timeout::timeout(60) do
  $stdout.sync = true
  # For xinetd
  Dir.chdir(File.dirname(__FILE__))

# {{{ === utility functions ===
  # str_to_num('AB') = 0x4142 = 16706
  def str_to_num(s)
    s.unpack('H*')[0].to_i(16)
  end

  # x^y (mod z)
  def pow(x, y, z)
    x.to_bn.mod_exp(y, z).to_i
  end

  # x^(-1) (mod y)
  def inv(x, y)
    x.to_bn.mod_inverse(y).to_i
  end

  def is_safe_prime(p)
    p.to_bn.prime? && ((p-1)/2).to_bn.prime?
  end
# }}}

# {{{ === proof of work ===
  # XXX: We only call this function once, no need to wrap it in a function.
  # def proof_of_work
    x = SecureRandom.random_bytes(6)
    puts 'Robot test'
    puts "prefix: #{[x].pack('m0')}"
    r = gets.strip.unpack('m0')[0]
    r = Digest::SHA1.digest(x + r)
    # We want the digest to begin with 23 bits of zero.
    # [0..15]
    unless r.start_with?("\0\0")
      puts 'FAIL! GO AWAY!'
      exit
    end
    c = r[2].ord
    r, s = c / 2, c % 2
    # r: [16..22], s: [23]
    unless r == 0
      puts 'FAIL! GO AWAY!'
      exit
    end
    print 'Good job! '
  # end
  # proof_of_work
# }}}

  # === Main starts here ===

  # Our safe prime.
  p = 285370232948523998980902649176998223002378361587332218493775786752826166161423082436982297888443231240619463576886971476889906175870272573060319231258784649665194518832695848032181036303102119334432612172767710672560390596241136280678425624046988433310588364872005613290545811367950034187020564546262381876467
  fail unless is_safe_prime(p)

  # Secret password
  # Although each password is small, we have 11 of them so we have 44 bits of entropy!
  passwords = IO.readlines('passwords').map(&:to_i)
  fail unless passwords.grep_v(1..16).empty?
  fail unless passwords.size == 11
  passwords.map!{|pass| Digest::SHA512.hexdigest(pass.to_s).to_i(16)}

  # More secrets!
  flag = IO.read('./flag1.txt').strip
  fail unless flag =~ /\Ahitcon\{[a-zA-Z0-9_]+\}\z/
  fail unless flag.size <= 60
  flag = str_to_num(flag)

  # Print banner
  puts
  puts 'This is a simple secret-flag-sharing server.'
  puts

  # This is the key to be xor-ed
  key = 0
  puts "p = #{p}"

  passwords.each.with_index(1) do |password, i|
    puts "Round #{i}"

    # Perform a simple PAKE handshake
    # You can find explanation in http://goo.gl/3foagq  (In code comment :D)

    w = pow(password, 2, p)  # NO to Legendre
    b = 2 + SecureRandom.random_number(p - 2)
    bb = pow(w, b, p)
    puts "Server send #{bb}"

    aa = gets.to_i
    if aa < 514 || aa >= p - 514
      puts 'CHEATER!'
      exit
    end

    k = pow(aa, b, p)
    key ^= Digest::SHA512.hexdigest(k.to_s).to_i(16)
  end

  # encrypt the flag!
  flag ^= key
  puts "Flag is (of course after encryption :D): #{flag}"

  # YAY!
  puts 'All done. Bye~'
  exit
end

# vim: fdm=marker:commentstring=\ \"\ %s:nowrap:autoread
