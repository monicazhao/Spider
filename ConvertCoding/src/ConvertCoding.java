import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Properties;

/**
 * 
 */

/**
 * @author monica
 *
 */
public class ConvertCoding {

	public static String readTxtFile(String filePath){
		
		String txtcontent = null;
        try {
                File file=new File(filePath);
                if(file.isFile() && file.exists()){ //判断文件是否存在
                    InputStreamReader readFile = new InputStreamReader(new FileInputStream(file));//考虑到编码格式
                    
                    Properties pp = new Properties();
                    pp.load(readFile);
                    txtcontent = pp.getProperty("service_comments").replaceAll("</?[^>]+>", "");
                    
                    readFile.close();
        }else{
            System.out.println("找不到指定的文件");
        }
        } catch (Exception e) {
            System.out.println("读取文件内容出错");
            e.printStackTrace();
        }
        return txtcontent;
    }
	
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		
		//读取目录下的所有文件
		File file=new File("F:\\result");
		File[] fileList = file.listFiles();
		
		//遍历目录下的所有文件，批量对txt文件进行处理
		for(int i = 0; i < fileList.length; i++){
			if(fileList[i].isFile()){
				String filePath = fileList[i].getPath();
				String result = readTxtFile(filePath);
				
				BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(filePath, true)));		
				out.write("\ncomments_info:" + result);
				out.close();
				System.out.println(result);
			}
		}
	}
}
