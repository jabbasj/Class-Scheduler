import java.net.MalformedURLException;
import java.net.URL;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.apache.commons.codec.binary.Base64;
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

public class profileTest{
	
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
	 * Enter intentionally wrong password, test the presence of a notification message
	 */
	@Test
	// Test: wrong old password
	public void invalidOldPassword(){
		
		/* cmVncmVzc2lvbg== equals the BASE64 encoded word: "regression", which does not 
		correspond to user's old password.*/ 
		testPassword ("cmVncmVzc2lvbg==", "Hello","Hello");

	}
	
	@Test
	// Test: wrong repeated password
	public void invalidRepeatedPassword(){
		
		// Even though the old password is correct, the new password does not correspond
		// to its repeated one.
		testPassword("cmVjZXNz", "World", "Hello");

	}
	
	@Test
	// Test: wrong new password
	public void invalidNewPassword(){
		
		// The new password is set to [empty]
		testPassword("cmVjZXNz", " ", " ");
	}
	
	public void testPassword (String oldPass, String newPass, String repeatPass){
		WebElement oldPwd, changePwd, newPwd, repeatPwd, notification;
		List <WebElement> submitButton;

		toProfilePage();
		changePwd = driver.findElement(By.xpath("//button[@onclick='change_password_overlay()']"));
		submitButton = driver.findElements(By.xpath("//button[@type='submit']"));
		changePwd.click();
		
		oldPwd = driver.findElement(By.xpath("//input[@id='id_old_password']"));
		newPwd = driver.findElement(By.xpath("//input[@id='id_new_password']"));
		repeatPwd = driver.findElement(By.xpath("//input[@id='id_repeat_new_password']"));
		
		oldPwd.sendKeys(decode(oldPass));
		newPwd.sendKeys(newPass);
		repeatPwd.sendKeys(repeatPass);
		
		submitButton.get(1).click();
		
		notification = driver.findElement(By.xpath("//div[@class='alert alert-danger']"));
		
		// Test the presence of the error notification message is shown
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[@class='alert alert-danger']")));
		Assert.assertTrue(notification.isDisplayed());
	}
	
	
	
	/**
	 * This method is intended to redirect to Profile page, the reason why it contains
	 * small unit tests is to increase efficacy and reusability of the current unit test. 
	 */
	public void toProfilePage(){
		String username = "vLasalle@gmail.com";
		// Encoded password
		String password = "cmVjZXNz";
		LoginPage loginPage = new LoginPage (driver);
		loginPage.toLoginPage(username, password);
		loginPage.login();
		
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//a[@href='/profile/']")));
		WebElement profile = driver.findElement(By.xpath("//a[@href='/profile/']"));
		// Test Profile button is click-enabled
		Assert.assertTrue(profile.isEnabled());
		profile.click();
		// Test the link redirect to Profile page
		WebElement title = driver.findElement(By.xpath("//h2"));
		Assert.assertTrue(title.getText().equals("Profile"));
	}
	
	/**
	 * This method decode the BASE64's generic term
	 * @param message
	 * @return decoded message
	 */
	public static String decode (String message){  
		byte[] decoded = Base64.decodeBase64(message);
		return new String (decoded);      
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


