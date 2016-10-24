#!/usr/bin/env ruby
#encoding: utf-8
require 'timeout'
require 'set'
$stdout.sync = true
$stdin.sync = true

N = 19
EMPTY = '．'
WH = '◯ '
BL = '⬤ '
DX = [0, 1, -1, 0]
DY = [1, 0, 0, -1]

class Object
  def deep_dup; dup; end
end

class Array
  def deep_dup; map(&:deep_dup); end
end

def flag
  puts "Congratulations!"
  puts IO.binread('flag')
  exit
end

def neighbor(x, y, i)
  a, b = x + DX[i], y + DY[i]
  return if a < 0 || a >= N || b < 0 || b >= N
  [a, b]
end

def alive?(brd, x, y, vst)
  vst.add [x, y]
  4.times do |i|
    a, b = neighbor(x, y, i)
    next if a.nil?
    return true if brd[a][b] == EMPTY
    next if brd[a][b] != brd[x][y]
    next if vst.member? [a, b]
    return true if alive?(brd, a, b, vst)
  end
  false
end

def capture?(_brd, hand)
  brd = _brd.deep_dup
  N.times do |x|
    N.times do |y|
      next if brd[x][y] == EMPTY || brd[x][y] == hand
      return true if not alive?(brd, x, y, Set.new)
      capture!(brd, x, y)
    end
  end
  false
end

def capture!(brd, x, y)
  hd = brd[x][y]
  brd[x][y] = EMPTY
  4.times do |i|
    a, b = neighbor(x, y, i)
    next if a.nil? or brd[a][b] != hd
    capture!(brd, a, b)
  end
end

def will_capture(_brd, x, y, hand)
  brd = _brd.deep_dup
  brd[x][y] = hand
  return true if capture?(brd, hand)
  false
end

def play?(_brd, x, y, hand)
  brd = _brd.deep_dup
  return false if brd[x][y] != EMPTY
  brd[x][y] = hand
  return true if capture?(brd, hand)
  return false if not alive?(brd, x, y, Set.new)
  true
end

def ai(brd, hand)
  return N/2, N/2 if brd.join.gsub(EMPTY, '').empty?
  x = N - 1 - @last_x
  y = N - 1 - @last_y
  return x, y if play?(brd, x, y, hand)
  cand = []
  N.times do |i|
    N.times do |j|
      next if brd[i][j] != EMPTY
      cand << [i, j] if play?(brd, i, j, hand)
    end
  end
  cand.sample
end

def show(brd)
  puts brd.map(&:join)
  true
end

def player(brd, hand)
  show(brd)
  s = $stdin.gets
  x, y = s.split.map(&:to_i)
  exit 1 if x < 0 || x >= N || y < 0 || y >= N
  exit 1 unless play?(brd, x, y, hand)
  [x, y]
end

def win(brd)
  b = brd.join
  b.count(WH) > b.count(BL)
end

def color_of(who)
  [BL, WH][who]
end

def exchg(cur)
  cur == WH ? BL : WH
end

def main
  brd = Array.new(N){Array.new(N){EMPTY}}
  who = 0
  loop do
    color = color_of who
    case who
    when 0 then x, y = ai(brd, color)
    when 1 then x, y = player(brd, color)
    else 
    end
    next if x.nil?
    brd[x][y] = color
    if who == 1 and will_capture(brd, x, y, color)
      puts "Isanagi activated!"
      brd[x][y] = exchg(brd[x][y])
    end
    N.times do |a|
      N.times do |b|
        next if brd[a][b] == EMPTY || brd[a][b] == color
        capture!(brd, a, b) if not alive?(brd, a, b, Set.new)
      end
    end
    @last_x, @last_y = x, y
    who ^= 1
    show(brd) and flag if win(brd)
  end
end

Timeout::timeout(180) { main }
