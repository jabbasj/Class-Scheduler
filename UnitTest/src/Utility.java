import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.ITestResult;

public class Utility {

	protected static WebDriver driver;
	protected WebDriverWait wait;
	protected static int numberOfScreenshot = 1;
	
	protected synchronized static void takeScreenShotOnFailure(ITestResult result) { 
		System.out.println("End of Test");
		if (result.getStatus() == ITestResult.FAILURE) {
			System.err.println("An error has been found.");
			String path = result.getTestContext().getOutputDirectory() + File.separator + result.getMethod().getMethodName() + "_screenshot" + numberOfScreenshot++ + ".png";
			System.err.println("Screenshot: " + path);
			try {
				File file = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
				FileUtils.copyFile(file, new File(path));
			} catch (WebDriverException e) {
				System.err.println("Cannot get screenshot: " + e.getMessage());
			} catch (IOException ex) {
				System.err.println("Error occurred when saving screenshot: " + ex.getMessage());
			}
		} 
		System.out.println(""); 
	}
	
	
}
