"""Statistics and probability operations module for advanced mathematical computations."""
import numpy as np
from scipy import stats
from scipy.stats import norm, binom, poisson, chi2, t, f
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError


def mean(data):
    """
    Calculate arithmetic mean of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        
    Returns:
        float: Mean value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
            
        # Calculate mean
        result = np.mean(arr)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate mean: {str(e)}")


def median(data):
    """
    Calculate median of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        
    Returns:
        float: Median value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
            
        # Calculate median
        result = np.median(arr)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate median: {str(e)}")


def mode(data):
    """
    Calculate mode of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        
    Returns:
        float: Mode value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
            
        # Calculate mode
        mode_result = stats.mode(arr, keepdims=True)
        return float(mode_result.mode[0])
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate mode: {str(e)}")


def variance(data, ddof=1):
    """
    Calculate variance of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        ddof (int): Delta degrees of freedom (0 for population, 1 for sample)
        
    Returns:
        float: Variance value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
        if arr.size <= ddof:
            raise ValidationError(f"Dataset size ({arr.size}) must be greater than ddof ({ddof})")
            
        # Calculate variance
        result = np.var(arr, ddof=ddof)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate variance: {str(e)}")


def standard_deviation(data, ddof=1):
    """
    Calculate standard deviation of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        ddof (int): Delta degrees of freedom (0 for population, 1 for sample)
        
    Returns:
        float: Standard deviation value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
        if arr.size <= ddof:
            raise ValidationError(f"Dataset size ({arr.size}) must be greater than ddof ({ddof})")
            
        # Calculate standard deviation
        result = np.std(arr, ddof=ddof)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate standard deviation: {str(e)}")


def correlation_coefficient(data_x, data_y):
    """
    Calculate Pearson correlation coefficient between two datasets.
    
    Args:
        data_x (list|np.ndarray): First dataset
        data_y (list|np.ndarray): Second dataset
        
    Returns:
        float: Correlation coefficient
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy arrays
        x = np.array(data_x)
        y = np.array(data_y)
        
        # Validate data
        if x.size == 0 or y.size == 0:
            raise ValidationError("Datasets cannot be empty")
        if x.size != y.size:
            raise ValidationError(f"Datasets must have same length: {x.size} vs {y.size}")
        if x.size < 2:
            raise ValidationError("Datasets must have at least 2 data points")
            
        # Calculate correlation coefficient
        correlation_matrix = np.corrcoef(x, y)
        correlation = correlation_matrix[0, 1]
        
        return float(correlation)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate correlation coefficient: {str(e)}")


def covariance(data_x, data_y, ddof=1):
    """
    Calculate covariance between two datasets.
    
    Args:
        data_x (list|np.ndarray): First dataset
        data_y (list|np.ndarray): Second dataset
        ddof (int): Delta degrees of freedom
        
    Returns:
        float: Covariance value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy arrays
        x = np.array(data_x)
        y = np.array(data_y)
        
        # Validate data
        if x.size == 0 or y.size == 0:
            raise ValidationError("Datasets cannot be empty")
        if x.size != y.size:
            raise ValidationError(f"Datasets must have same length: {x.size} vs {y.size}")
        if x.size <= ddof:
            raise ValidationError(f"Dataset size ({x.size}) must be greater than ddof ({ddof})")
            
        # Calculate covariance
        covariance_matrix = np.cov(x, y, ddof=ddof)
        cov = covariance_matrix[0, 1]
        
        return float(cov)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate covariance: {str(e)}")


def normal_distribution_pdf(x, mean=0, std=1):
    """
    Calculate probability density function of normal distribution.
    
    Args:
        x (float): Value to evaluate
        mean (float): Mean of the distribution
        std (float): Standard deviation of the distribution
        
    Returns:
        float: PDF value
        
    Raises:
        ValidationError: If parameters are invalid
        CalculationError: If calculation fails
    """
    try:
        # Validate inputs
        validate_numbers(x, mean, std)
        if std <= 0:
            raise ValidationError("Standard deviation must be positive")
            
        # Calculate PDF
        result = norm.pdf(x, loc=mean, scale=std)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate normal PDF: {str(e)}")


def normal_distribution_cdf(x, mean=0, std=1):
    """
    Calculate cumulative distribution function of normal distribution.
    
    Args:
        x (float): Value to evaluate
        mean (float): Mean of the distribution
        std (float): Standard deviation of the distribution
        
    Returns:
        float: CDF value
        
    Raises:
        ValidationError: If parameters are invalid
        CalculationError: If calculation fails
    """
    try:
        # Validate inputs
        validate_numbers(x, mean, std)
        if std <= 0:
            raise ValidationError("Standard deviation must be positive")
            
        # Calculate CDF
        result = norm.cdf(x, loc=mean, scale=std)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate normal CDF: {str(e)}")


def binomial_distribution_pmf(k, n, p):
    """
    Calculate probability mass function of binomial distribution.
    
    Args:
        k (int): Number of successes
        n (int): Number of trials
        p (float): Probability of success
        
    Returns:
        float: PMF value
        
    Raises:
        ValidationError: If parameters are invalid
        CalculationError: If calculation fails
    """
    try:
        # Validate inputs
        if not isinstance(k, int) or not isinstance(n, int):
            raise ValidationError("k and n must be integers")
        if k < 0 or n < 0 or k > n:
            raise ValidationError("Invalid parameters: k and n must be non-negative and k <= n")
        validate_numbers(p)
        if p < 0 or p > 1:
            raise ValidationError("Probability p must be between 0 and 1")
            
        # Calculate PMF
        result = binom.pmf(k, n, p)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate binomial PMF: {str(e)}")


def poisson_distribution_pmf(k, mu):
    """
    Calculate probability mass function of Poisson distribution.
    
    Args:
        k (int): Number of events
        mu (float): Mean rate parameter
        
    Returns:
        float: PMF value
        
    Raises:
        ValidationError: If parameters are invalid
        CalculationError: If calculation fails
    """
    try:
        # Validate inputs
        if not isinstance(k, int) or k < 0:
            raise ValidationError("k must be a non-negative integer")
        validate_numbers(mu)
        if mu <= 0:
            raise ValidationError("Rate parameter mu must be positive")
            
        # Calculate PMF
        result = poisson.pmf(k, mu)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate Poisson PMF: {str(e)}")


def t_test_one_sample(data, population_mean, alpha=0.05):
    """
    Perform one-sample t-test.
    
    Args:
        data (list|np.ndarray): Sample data
        population_mean (float): Hypothesized population mean
        alpha (float): Significance level
        
    Returns:
        dict: Test results including t-statistic, p-value, and conclusion
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If test fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
        if arr.size < 2:
            raise ValidationError("Dataset must have at least 2 data points")
        validate_numbers(population_mean, alpha)
        if alpha <= 0 or alpha >= 1:
            raise ValidationError("Alpha must be between 0 and 1")
            
        # Perform t-test
        t_statistic, p_value = stats.ttest_1samp(arr, population_mean)
        
        # Determine conclusion
        reject_null = p_value < alpha
        
        return {
            't_statistic': float(t_statistic),
            'p_value': float(p_value),
            'alpha': alpha,
            'reject_null': reject_null,
            'conclusion': 'Reject null hypothesis' if reject_null else 'Fail to reject null hypothesis'
        }
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to perform one-sample t-test: {str(e)}")


def t_test_two_sample(data1, data2, alpha=0.05, equal_var=True):
    """
    Perform two-sample t-test.
    
    Args:
        data1 (list|np.ndarray): First sample data
        data2 (list|np.ndarray): Second sample data
        alpha (float): Significance level
        equal_var (bool): Whether to assume equal variances
        
    Returns:
        dict: Test results including t-statistic, p-value, and conclusion
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If test fails
    """
    try:
        # Convert to numpy arrays
        arr1 = np.array(data1)
        arr2 = np.array(data2)
        
        # Validate data
        if arr1.size == 0 or arr2.size == 0:
            raise ValidationError("Datasets cannot be empty")
        if arr1.size < 2 or arr2.size < 2:
            raise ValidationError("Datasets must have at least 2 data points")
        validate_numbers(alpha)
        if alpha <= 0 or alpha >= 1:
            raise ValidationError("Alpha must be between 0 and 1")
            
        # Perform t-test
        t_statistic, p_value = stats.ttest_ind(arr1, arr2, equal_var=equal_var)
        
        # Determine conclusion
        reject_null = p_value < alpha
        
        return {
            't_statistic': float(t_statistic),
            'p_value': float(p_value),
            'alpha': alpha,
            'equal_var': equal_var,
            'reject_null': reject_null,
            'conclusion': 'Reject null hypothesis' if reject_null else 'Fail to reject null hypothesis'
        }
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to perform two-sample t-test: {str(e)}")


def chi_square_test(observed, expected=None, alpha=0.05):
    """
    Perform chi-square goodness-of-fit test.
    
    Args:
        observed (list|np.ndarray): Observed frequencies
        expected (list|np.ndarray): Expected frequencies (optional)
        alpha (float): Significance level
        
    Returns:
        dict: Test results including chi-square statistic, p-value, and conclusion
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If test fails
    """
    try:
        # Convert to numpy arrays
        obs = np.array(observed)
        
        # Validate data
        if obs.size == 0:
            raise ValidationError("Observed frequencies cannot be empty")
        if np.any(obs < 0):
            raise ValidationError("Observed frequencies must be non-negative")
        validate_numbers(alpha)
        if alpha <= 0 or alpha >= 1:
            raise ValidationError("Alpha must be between 0 and 1")
            
        # Handle expected frequencies
        if expected is None:
            # Uniform distribution
            exp = np.full(obs.size, np.sum(obs) / obs.size)
        else:
            exp = np.array(expected)
            if exp.size != obs.size:
                raise ValidationError("Observed and expected frequencies must have same length")
            if np.any(exp <= 0):
                raise ValidationError("Expected frequencies must be positive")
                
        # Perform chi-square test
        chi2_statistic, p_value = stats.chisquare(obs, exp)
        
        # Determine conclusion
        reject_null = p_value < alpha
        
        return {
            'chi2_statistic': float(chi2_statistic),
            'p_value': float(p_value),
            'alpha': alpha,
            'degrees_of_freedom': obs.size - 1,
            'reject_null': reject_null,
            'conclusion': 'Reject null hypothesis' if reject_null else 'Fail to reject null hypothesis'
        }
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to perform chi-square test: {str(e)}")


def linear_regression(x_data, y_data):
    """
    Perform linear regression analysis.
    
    Args:
        x_data (list|np.ndarray): Independent variable data
        y_data (list|np.ndarray): Dependent variable data
        
    Returns:
        dict: Regression results including slope, intercept, R-squared, and predictions
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If regression fails
    """
    try:
        # Convert to numpy arrays
        x = np.array(x_data)
        y = np.array(y_data)
        
        # Validate data
        if x.size == 0 or y.size == 0:
            raise ValidationError("Datasets cannot be empty")
        if x.size != y.size:
            raise ValidationError(f"Datasets must have same length: {x.size} vs {y.size}")
        if x.size < 2:
            raise ValidationError("Datasets must have at least 2 data points")
            
        # Reshape for sklearn
        X = x.reshape(-1, 1)
        
        # Perform linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Get predictions
        y_pred = model.predict(X)
        
        # Calculate R-squared
        r_squared = model.score(X, y)
        
        # Calculate residuals
        residuals = y - y_pred
        
        return {
            'slope': float(model.coef_[0]),
            'intercept': float(model.intercept_),
            'r_squared': float(r_squared),
            'predictions': y_pred.tolist(),
            'residuals': residuals.tolist()
        }
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to perform linear regression: {str(e)}")


def confidence_interval(data, confidence_level=0.95):
    """
    Calculate confidence interval for the mean.
    
    Args:
        data (list|np.ndarray): Sample data
        confidence_level (float): Confidence level (e.g., 0.95 for 95%)
        
    Returns:
        dict: Confidence interval results
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
        if arr.size < 2:
            raise ValidationError("Dataset must have at least 2 data points")
        validate_numbers(confidence_level)
        if confidence_level <= 0 or confidence_level >= 1:
            raise ValidationError("Confidence level must be between 0 and 1")
            
        # Calculate statistics
        sample_mean = np.mean(arr)
        sample_std = np.std(arr, ddof=1)
        n = len(arr)
        
        # Calculate confidence interval using t-distribution
        alpha = 1 - confidence_level
        t_critical = stats.t.ppf(1 - alpha/2, n - 1)
        margin_of_error = t_critical * (sample_std / np.sqrt(n))
        
        lower_bound = sample_mean - margin_of_error
        upper_bound = sample_mean + margin_of_error
        
        return {
            'mean': float(sample_mean),
            'std': float(sample_std),
            'confidence_level': confidence_level,
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'margin_of_error': float(margin_of_error)
        }
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate confidence interval: {str(e)}")


def z_score(value, mean, std):
    """
    Calculate z-score (standard score).
    
    Args:
        value (float): Value to standardize
        mean (float): Mean of the distribution
        std (float): Standard deviation of the distribution
        
    Returns:
        float: Z-score
        
    Raises:
        ValidationError: If parameters are invalid
        CalculationError: If calculation fails
    """
    try:
        # Validate inputs
        validate_numbers(value, mean, std)
        if std <= 0:
            raise ValidationError("Standard deviation must be positive")
            
        # Calculate z-score
        z = (value - mean) / std
        return float(z)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate z-score: {str(e)}")


def percentile(data, percentile_value):
    """
    Calculate percentile of a dataset.
    
    Args:
        data (list|np.ndarray): Dataset
        percentile_value (float): Percentile to calculate (0-100)
        
    Returns:
        float: Percentile value
        
    Raises:
        ValidationError: If data is invalid
        CalculationError: If calculation fails
    """
    try:
        # Convert to numpy array
        arr = np.array(data)
        
        # Validate data
        if arr.size == 0:
            raise ValidationError("Dataset cannot be empty")
        validate_numbers(percentile_value)
        if percentile_value < 0 or percentile_value > 100:
            raise ValidationError("Percentile must be between 0 and 100")
            
        # Calculate percentile
        result = np.percentile(arr, percentile_value)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to calculate percentile: {str(e)}")
