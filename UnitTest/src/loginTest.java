import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Select;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.testng.ITestResult;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class loginTest{
	
	protected WebDriver driver;
	protected DesiredCapabilities capability; 
	protected int timer;
	protected WebDriverWait wait;
	
	@BeforeMethod 
	public void setUp () throws InterruptedException, MalformedURLException{
		capability = DesiredCapabilities.firefox();	     
		capability.setPlatform(org.openqa.selenium.Platform.WINDOWS);
		driver = new RemoteWebDriver(new URL("http://localhost:4444/wd/hub"), capability);
		
		wait = new WebDriverWait(driver, 20);
		driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
		driver.manage().window().maximize();
		
	}
	

	@Test
	public void invalidUsername (){
		String username = "dLasalle@gmail.com";
		// Encoded password
		String password = "cmVjZXNz";
		
		LoginPage loginPage = new LoginPage (driver);
		loginPage.toLoginPage(username, password);
	}
	
	@Test
	public void invalidPassword (){
		String username = "vLasalle@gmail.com";
		// Encoded password
		String password = "cmVncmVzc2lvbg==";
		
		LoginPage loginPage = new LoginPage (driver);
		loginPage.toLoginPage(username, password);
	}
	
	@Test
	public void emptyPasswordUsername(){
		String username = " ";
		String password = " ";
		
		LoginPage loginPage = new LoginPage (driver);
		loginPage.toLoginPage(username, password);
	}
	
	// Take a screen shot if the test fails
	@AfterMethod 
	public void takeScreenShot(ITestResult result) { 
		Utility.takeScreenShotOnFailure(result);
	} 

	// Close driver
	@AfterClass 
	public void tearDown (){
		driver.quit();
	}
}


