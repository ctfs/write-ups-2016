-- http://www.playwithlua.com/?p=28

function make_board(size)
   local board = { size = size }
   setmetatable(board, { __tostring = board_tostring })

   for n = 0, size * size - 1 do
      board[n] = 0
   end

   return board
end

function populate_board(board, filled, seed)
   local size = board.size
   if seed then math.randomseed(seed) end
   filled = filled or size * size * 3 / 4

   local function rand()
      local c
      repeat c = math.random(size * size) - 1 until board[c] == 0
      return c
   end

   if filled > 0 then
      for _,v in ipairs{'a','b','c','d'} do board[rand()] = v end

      for n = 1, filled-4 do
         board[rand()] = math.random(4)
      end

      return fall(board)
   end
end

function board_tostring(board)
   local lines = {}
   local size = board.size
   for y = 0, size - 1 do
      local line = "|"
      for x = 0, size - 1 do
         line = line .. " " .. board[x+y*size]
      end
      table.insert(lines, line .. " |")
   end
   return table.concat(lines,"\n")
end

function fall(board)
   local size = board.size
   local new_board = make_board(size, 0)

   local function fall_column(col)
      local dest = size - 1
      for y = size-1, 0, -1 do
         if board[y*size + col] ~= 0 then
            new_board[dest*size + col] = board[y*size + col]
            dest = dest - 1
         end
      end
   end

   for x=0, size-1 do
      fall_column(x)
   end

   return new_board
end

function rotate(board)
   local size = board.size
   local new_board = make_board(size, 0)

   for y = 0, size-1 do
      local dest_col = size - 1 - y

      for n = 0, size-1 do
         new_board[n*size + dest_col] = board[y*size + n]
      end
   end

   return new_board
end

function crush(board)
   local size = board.size
   local new_board = make_board(size, 0)
   local crushers = {'a','b','c','d'}

   for n=0, size-1 do
      new_board[n] = board[n]
   end

   for n = size, size*size - 1 do
      if board[n-size] == crushers[board[n]] then
         new_board[n] = 0
      else
         new_board[n] = board[n]
      end
   end

   return new_board
end

function rotate_left(board)
   return rotate(rotate(rotate(board)))
end

function readAll(file)
    local f = io.open(file, "rb")
    local content = f:read("*all")
    f:close()
    return content
end

function help()
	local l = string.sub(readAll("server.luac"), 2)

	writeraw(l, string.len(l))
end

quit = false
function exit()
	quit = true
end

function run_step(board)
   local cmd = readline()

   if(string.len(cmd) == 0) then
   	 exit()
   	 return nil
   end

   -- prevent injection attacks
   if(string.find(cmd, "function")) then
   	 return nil
   end

   if(string.find(cmd, "print")) then
   	 return nil
   end

   local f = load("return " .. cmd)()

   if f == nil then
   	 return nil
   end

   return f(board)
end

function game()
   local board = populate_board(make_board(8))

   repeat
      
      writeline(board_tostring(board) .. "\n")
      
      local b = run_step(board)

      if quit then
      	break
      end

      if b ~= nil then
      	 board = b
         board = fall(crush(fall(board)))
      else
         writeline("Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.\n")
      end

   until false
end

writeline("let's play a game\n")

game()
