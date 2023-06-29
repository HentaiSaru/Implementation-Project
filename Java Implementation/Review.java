public class Review{
    public static void main(String[] args){

        int sum = 0 , sum2 = 0;
        for(int i=0;i<=100;i++){
            if(i % 2 == 0){
                sum += i;
            }else{
                sum2 += i;
            }
            
        }
        System.out.printf("偶數總和 : %d , 基數總和 %d" , sum , sum2);
    }
}