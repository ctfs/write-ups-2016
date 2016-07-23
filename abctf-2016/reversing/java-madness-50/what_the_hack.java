public class what_the_hack {

	public static void main(String[] args) {
		
		String check = "";
		
		if(args.length != 5){
			System.out.println("Almost! (;");
		}
		
		else {
			for(int i = args.length - 1; i >= 0; i--){
				System.out.println(i);
				for(int j = args[i].length() - 1; j >= 0; j--){
					check += args[i].charAt(j);
					System.out.println(args[i].charAt(j));
				}
			}
			
			if(check.equals("abctf is the coolest ctf")){
				System.out.println("Flag: " + "ABCTF{" + args[0] + args[1] + args[2] +args[3] + args[4] + "}");
			}
			else{
				System.out.println(check);
			}
		}
	}
}

