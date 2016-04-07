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
import org.testng.Assert;
import org.testng.ITestResult;
import org.testng.annotations.AfterClass;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

public class logoutTest{
	
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
	

	/**
	 * Test: Check no defectives output is present
	 */
	@Test
	public void noDefects (){
		//Log in --------------------------------------
		String username = "vLasalle@gmail.com";
		// Encoded password
		String password = "cmVjZXNz";
		
		LoginPage loginPage = new LoginPage (driver);
		loginPage.toLoginPage(username, password);
		loginPage.login();
		//--------------------------------------------

		WebElement logoutButton = driver.findElement(By.xpath("//a[contains(.,'Log off')]"));
		logoutButton.click();
		
		Assert.assertTrue(profileInvisible("//a[contains(.,'Hello, Vince!')]"));
		Assert.assertTrue(loginButtonAvailable());
		Assert.assertTrue(logoutButtonUnavailable("//a[contains(.,'Log off')]"));
	}
	

	
	// Make sure user information is invisible after log out
	/**
	 * Wait until profile becomes invisible to user, if profile is still visible after 30 seconds
	 * of checking, an error will be thrown, the test will fail.
	 * 
	 * @param profile
	 * @return true if the test is successful
	 */
	public boolean profileInvisible (String profileXpath){
		wait.until(ExpectedConditions.invisibilityOfElementLocated(By.xpath(profileXpath)));
		return true;
	}
	
	/**
	 * Wait until login button becomes visible to user, if login is still invisible after 30 seconds
	 * of checking, an error will be thrown, the test will fail.
	 * 
	 * @return true if the test is successful
	 */
	public boolean loginButtonAvailable (){
		// WebElement login has the following xpath: "//a[@href='/login/']"
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//a[@href='/login/']")));
		return true;
	}
	
	/**
	 * Wait until log out becomes invisible to user, if log out is still visible after 30 seconds
	 * of checking, an error will be thrown, the test will fail.
	 * 
	 * @param logout
	 * @return true if the test is successful
	 */
	public boolean logoutButtonUnavailable (String logoutXpath){
		wait.until(ExpectedConditions.invisibilityOfElementLocated(By.xpath(logoutXpath)));
		return true;
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


