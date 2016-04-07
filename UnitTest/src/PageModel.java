
import java.util.ArrayList;
import org.apache.commons.codec.binary.Base64;
import org.openqa.selenium.By;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

// Tab helper class
public abstract class PageModel {

	protected WebDriver driver;
	protected WebDriverWait wait;
	private static final int maxRetries = 5;
	
	public PageModel(WebDriver driver, long waitSeconds) {
		this.driver = driver;
		wait = new WebDriverWait(driver, waitSeconds);
	}

	// Decode the hashed password
	public static String decode (String message){  
		byte[] decoded = Base64.decodeBase64(message);
		return new String (decoded);      
	}

	// Wait until the element defined by xpath is present
	@Deprecated
	public static void waitUntil(String xpath, WebDriverWait wait){
		wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(xpath)));
	}
	
	// Wait until the element defined by xpath is present
	public void waitUntil(String xpath){
		wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(xpath)));
	}
	
	// Close current focused tab
	@Deprecated
	public static void closeTab (WebDriver driver){
		driver.close();
	}
	
	// Close current focused tab
	public void closeTab (){
		driver.close();
	}

	// Switch to tab index number
	@Deprecated
	public static void switchToTab (WebDriver driver, int tabIndex){
		ArrayList<String> tabs = new ArrayList<String> (driver.getWindowHandles());
		driver.switchTo().window(tabs.get(tabIndex));
	}
	
	// Switch to tab index number
	public void switchToTab (int tabIndex){
		ArrayList<String> tabs = new ArrayList<String> (driver.getWindowHandles());
		driver.switchTo().window(tabs.get(tabIndex));
	}
	
	public void switchTab() {
		String current = driver.getWindowHandle();
		for (String it : driver.getWindowHandles()) {
			if (!it.equals(current)) {
				driver.switchTo().window(it);
				break;
			}
		}
	}

	// Wait for a given number of windows / tabs
	@Deprecated
	public static void waitForTabEqual( WebDriver driver, final int tabIndex) {
		new WebDriverWait(driver, 1000) {
		}.until(new ExpectedCondition<Boolean>() {
			@Override
			public Boolean apply(WebDriver driver) {                        
				return (driver.getWindowHandles().size() == tabIndex);
			}
		});
	}
	
	// Wait for a given number of windows / tabs
	public void waitForTabEqual(final int numberOfTabs) {
		new WebDriverWait(driver, 1000) {
		}.until(new ExpectedCondition<Boolean>() {
			@Override
			public Boolean apply(WebDriver driver) {                        
				return (driver.getWindowHandles().size() == numberOfTabs);
			}
		});
	}
	
	public void waitUntilWithRefresh(String xpath){
		int retries = 0;
		while (retries < maxRetries) {
			try {
				if (retries != 0) {
					driver.navigate().refresh();
				}
				wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(xpath)));
				return;
			} catch (TimeoutException e) {
				retries++;
			}
		}
		throw new TimeoutException("Maximum number of retries exceeded");
	}


}
