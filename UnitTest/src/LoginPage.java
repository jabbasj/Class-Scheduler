
import org.junit.Assert;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class LoginPage extends PageModel{
	
	WebElement header;
	private String username = "";;
	private String password = "";
	private String baseUrl="http://52.11.49.193/";
	private WebElement loginButton, notification;

	
	public LoginPage (WebDriver driver){
		super(driver,10);
	}
	
	public void toLoginPage (String username,String password){
		this.username = username;
		this.password = decode(password);
		
		toLoginPage();
		// Click on login button
		try{
			driver.findElement(By.xpath("//a[contains(.,'Log in')]")).isDisplayed();
			loginButton = driver.findElement(By.xpath("//a[contains(.,'Log in')]"));
			
			//Check if Log in button is present
			System.out.println(loginButton.getText());
			Assert.assertTrue(loginButton.getText().equals("Log in"));
			Assert.assertTrue(loginButton.isEnabled());
		}catch(TimeoutException | NoSuchElementException e){
		}
		loginButton.click();
	}
	
	public void login (){
		driver.findElement(By.xpath("//input[@id='id_username']")).click();
		driver.findElement(By.id("id_username")).clear();
		driver.findElement(By.id("id_username")).sendKeys(username);    
		driver.findElement(By.id("id_password")).click();
		driver.findElement(By.id("id_password")).clear();
		driver.findElement(By.id("id_password")).sendKeys(password);
		driver.findElement(By.xpath("//input[@value='Log in']")).click();
	}
	
	public void check(){
		header = driver.findElement(By.xpath("//h2[contains(.,'Lotus is a schedule "
				+ "generator for Software Engineering students.')]"));
		header.isDisplayed();
		System.out.println("Currently on the Login Page...");
	}
	

	public void toLoginPage (){
		driver.get(baseUrl);
		check();
	}
	
	public void errorNotification (String username, String password){
		driver.findElement(By.xpath("//input[@id='id_username']")).click();
		driver.findElement(By.id("id_username")).clear();
		driver.findElement(By.id("id_username")).sendKeys(username);    
		driver.findElement(By.id("id_password")).click();
		driver.findElement(By.id("id_password")).clear();
		driver.findElement(By.id("id_password")).sendKeys(password);
		driver.findElement(By.xpath("//input[@value='Log in']")).click();
		
		wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//p[@class='validation-summary-errors']")));
		notification = driver.findElement(By.xpath("//p[@class='validation-summary-errors']"));
		Assert.assertNotEquals(notification.getText(), "Please enter a correct user name and password");
	}

}

