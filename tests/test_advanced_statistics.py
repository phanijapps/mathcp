"""Test suite for advanced statistics and probability operations."""
import pytest
import numpy as np
from mathgenius.advanced.statistics import (
    mean, median, mode, variance, standard_deviation,
    correlation_coefficient, covariance, normal_distribution_pdf,
    normal_distribution_cdf, binomial_distribution_pmf, poisson_distribution_pmf,
    t_test_one_sample, t_test_two_sample, chi_square_test, linear_regression,
    confidence_interval, z_score, percentile
)
from mathgenius.core.errors import ValidationError, CalculationError


class TestDescriptiveStatistics:
    """Test descriptive statistics functions."""
    
    def test_mean_basic(self):
        """Test mean calculation."""
        data = [1, 2, 3, 4, 5]
        result = mean(data)
        expected = 3.0
        assert abs(result - expected) < 1e-10
    
    def test_mean_empty_data(self):
        """Test mean with empty data."""
        with pytest.raises(ValidationError):
            mean([])
    
    def test_median_basic(self):
        """Test median calculation."""
        # Odd number of elements
        data = [1, 2, 3, 4, 5]
        result = median(data)
        expected = 3.0
        assert abs(result - expected) < 1e-10
        
        # Even number of elements
        data = [1, 2, 3, 4]
        result = median(data)
        expected = 2.5
        assert abs(result - expected) < 1e-10
    
    def test_median_empty_data(self):
        """Test median with empty data."""
        with pytest.raises(ValidationError):
            median([])
    
    def test_mode_basic(self):
        """Test mode calculation."""
        data = [1, 2, 2, 3, 3, 3, 4]
        result = mode(data)
        expected = 3.0  # Most frequent value
        assert abs(result - expected) < 1e-10
    
    def test_mode_empty_data(self):
        """Test mode with empty data."""
        with pytest.raises(ValidationError):
            mode([])
    
    def test_variance_basic(self):
        """Test variance calculation."""
        data = [1, 2, 3, 4, 5]
        result = variance(data, ddof=1)  # Sample variance
        expected = 2.5  # Sample variance of [1,2,3,4,5]
        assert abs(result - expected) < 1e-10
        
        # Population variance
        result = variance(data, ddof=0)
        expected = 2.0  # Population variance
        assert abs(result - expected) < 1e-10
    
    def test_variance_empty_data(self):
        """Test variance with empty data."""
        with pytest.raises(ValidationError):
            variance([])
    
    def test_variance_insufficient_data(self):
        """Test variance with insufficient data."""
        with pytest.raises(ValidationError):
            variance([1], ddof=1)  # Need at least 2 data points for sample variance
    
    def test_standard_deviation_basic(self):
        """Test standard deviation calculation."""
        data = [1, 2, 3, 4, 5]
        result = standard_deviation(data, ddof=1)
        expected = np.sqrt(2.5)  # sqrt of sample variance
        assert abs(result - expected) < 1e-10
    
    def test_standard_deviation_empty_data(self):
        """Test standard deviation with empty data."""
        with pytest.raises(ValidationError):
            standard_deviation([])


class TestCorrelationCovariance:
    """Test correlation and covariance functions."""
    
    def test_correlation_coefficient_basic(self):
        """Test correlation coefficient calculation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]  # Perfect positive correlation
        result = correlation_coefficient(x, y)
        expected = 1.0
        assert abs(result - expected) < 1e-10
    
    def test_correlation_coefficient_negative(self):
        """Test negative correlation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]  # Perfect negative correlation
        result = correlation_coefficient(x, y)
        expected = -1.0
        assert abs(result - expected) < 1e-10
    
    def test_correlation_coefficient_mismatched_size(self):
        """Test correlation with mismatched data sizes."""
        x = [1, 2, 3]
        y = [2, 4, 6, 8]
        with pytest.raises(ValidationError):
            correlation_coefficient(x, y)
    
    def test_correlation_coefficient_insufficient_data(self):
        """Test correlation with insufficient data."""
        x = [1]
        y = [2]
        with pytest.raises(ValidationError):
            correlation_coefficient(x, y)
    
    def test_covariance_basic(self):
        """Test covariance calculation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = covariance(x, y, ddof=1)
        
        # Should be positive (positive relationship)
        assert result > 0
    
    def test_covariance_mismatched_size(self):
        """Test covariance with mismatched data sizes."""
        x = [1, 2, 3]
        y = [2, 4, 6, 8]
        with pytest.raises(ValidationError):
            covariance(x, y)


class TestProbabilityDistributions:
    """Test probability distribution functions."""
    
    def test_normal_distribution_pdf_basic(self):
        """Test normal distribution PDF."""
        # Standard normal distribution at x=0
        result = normal_distribution_pdf(0, mean=0, std=1)
        expected = 1 / np.sqrt(2 * np.pi)  # PDF of standard normal at 0
        assert abs(result - expected) < 1e-10
    
    def test_normal_distribution_pdf_invalid_std(self):
        """Test normal PDF with invalid standard deviation."""
        with pytest.raises(ValidationError):
            normal_distribution_pdf(0, mean=0, std=0)
        
        with pytest.raises(ValidationError):
            normal_distribution_pdf(0, mean=0, std=-1)
    
    def test_normal_distribution_cdf_basic(self):
        """Test normal distribution CDF."""
        # Standard normal distribution at x=0 should be 0.5
        result = normal_distribution_cdf(0, mean=0, std=1)
        expected = 0.5
        assert abs(result - expected) < 1e-10
    
    def test_normal_distribution_cdf_invalid_std(self):
        """Test normal CDF with invalid standard deviation."""
        with pytest.raises(ValidationError):
            normal_distribution_cdf(0, mean=0, std=0)
    
    def test_binomial_distribution_pmf_basic(self):
        """Test binomial distribution PMF."""
        # Binomial(n=10, p=0.5) at k=5
        result = binomial_distribution_pmf(5, 10, 0.5)
        expected = 0.24609375  # Exact value for this case
        assert abs(result - expected) < 1e-6
    
    def test_binomial_distribution_pmf_invalid_parameters(self):
        """Test binomial PMF with invalid parameters."""
        # Invalid k or n
        with pytest.raises(ValidationError):
            binomial_distribution_pmf(-1, 10, 0.5)
        
        with pytest.raises(ValidationError):
            binomial_distribution_pmf(11, 10, 0.5)  # k > n
        
        # Invalid p
        with pytest.raises(ValidationError):
            binomial_distribution_pmf(5, 10, -0.1)
        
        with pytest.raises(ValidationError):
            binomial_distribution_pmf(5, 10, 1.1)
    
    def test_poisson_distribution_pmf_basic(self):
        """Test Poisson distribution PMF."""
        # Poisson(μ=2) at k=2
        result = poisson_distribution_pmf(2, 2)
        expected = 2**2 * np.exp(-2) / np.math.factorial(2)
        assert abs(result - expected) < 1e-10
    
    def test_poisson_distribution_pmf_invalid_parameters(self):
        """Test Poisson PMF with invalid parameters."""
        # Invalid k
        with pytest.raises(ValidationError):
            poisson_distribution_pmf(-1, 2)
        
        # Invalid μ
        with pytest.raises(ValidationError):
            poisson_distribution_pmf(2, 0)
        
        with pytest.raises(ValidationError):
            poisson_distribution_pmf(2, -1)


class TestHypothesisTesting:
    """Test hypothesis testing functions."""
    
    def test_t_test_one_sample_basic(self):
        """Test one-sample t-test."""
        # Data that should be significantly different from population mean
        data = [1, 2, 3, 4, 5]
        population_mean = 0
        result = t_test_one_sample(data, population_mean)
        
        # Should have these keys
        assert 't_statistic' in result
        assert 'p_value' in result
        assert 'alpha' in result
        assert 'reject_null' in result
        assert 'conclusion' in result
        
        # Should reject null hypothesis (mean != 0)
        assert result['reject_null'] == True
    
    def test_t_test_one_sample_insufficient_data(self):
        """Test one-sample t-test with insufficient data."""
        with pytest.raises(ValidationError):
            t_test_one_sample([1], 0)
    
    def test_t_test_one_sample_invalid_alpha(self):
        """Test one-sample t-test with invalid alpha."""
        data = [1, 2, 3, 4, 5]
        with pytest.raises(ValidationError):
            t_test_one_sample(data, 0, alpha=0)
        
        with pytest.raises(ValidationError):
            t_test_one_sample(data, 0, alpha=1)
    
    def test_t_test_two_sample_basic(self):
        """Test two-sample t-test."""
        # Two different samples
        data1 = [1, 2, 3, 4, 5]
        data2 = [6, 7, 8, 9, 10]
        result = t_test_two_sample(data1, data2)
        
        # Should have these keys
        assert 't_statistic' in result
        assert 'p_value' in result
        assert 'alpha' in result
        assert 'equal_var' in result
        assert 'reject_null' in result
        assert 'conclusion' in result
        
        # Should reject null hypothesis (means are different)
        assert result['reject_null'] == True
    
    def test_t_test_two_sample_insufficient_data(self):
        """Test two-sample t-test with insufficient data."""
        with pytest.raises(ValidationError):
            t_test_two_sample([1], [2, 3])
    
    def test_chi_square_test_basic(self):
        """Test chi-square goodness-of-fit test."""
        # Observed frequencies
        observed = [10, 15, 20, 25]
        # Expected frequencies (uniform distribution)
        expected = [17.5, 17.5, 17.5, 17.5]
        
        result = chi_square_test(observed, expected)
        
        # Should have these keys
        assert 'chi2_statistic' in result
        assert 'p_value' in result
        assert 'alpha' in result
        assert 'degrees_of_freedom' in result
        assert 'reject_null' in result
        assert 'conclusion' in result
    
    def test_chi_square_test_invalid_frequencies(self):
        """Test chi-square test with invalid frequencies."""
        # Negative observed frequencies
        with pytest.raises(ValidationError):
            chi_square_test([-1, 2, 3], [2, 2, 2])
        
        # Zero expected frequencies
        with pytest.raises(ValidationError):
            chi_square_test([1, 2, 3], [0, 2, 2])
    
    def test_chi_square_test_mismatched_sizes(self):
        """Test chi-square test with mismatched sizes."""
        with pytest.raises(ValidationError):
            chi_square_test([1, 2, 3], [2, 2])


class TestRegression:
    """Test regression analysis functions."""
    
    def test_linear_regression_basic(self):
        """Test linear regression."""
        # Perfect linear relationship: y = 2x + 1
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 7, 9, 11]
        
        result = linear_regression(x, y)
        
        # Should have these keys
        assert 'slope' in result
        assert 'intercept' in result
        assert 'r_squared' in result
        assert 'predictions' in result
        assert 'residuals' in result
        
        # Should find correct slope and intercept
        assert abs(result['slope'] - 2.0) < 1e-10
        assert abs(result['intercept'] - 1.0) < 1e-10
        
        # Should have perfect fit (R² = 1)
        assert abs(result['r_squared'] - 1.0) < 1e-10
    
    def test_linear_regression_insufficient_data(self):
        """Test linear regression with insufficient data."""
        with pytest.raises(ValidationError):
            linear_regression([1], [2])
    
    def test_linear_regression_mismatched_sizes(self):
        """Test linear regression with mismatched sizes."""
        with pytest.raises(ValidationError):
            linear_regression([1, 2, 3], [4, 5])


class TestConfidenceInterval:
    """Test confidence interval calculation."""
    
    def test_confidence_interval_basic(self):
        """Test confidence interval calculation."""
        data = [1, 2, 3, 4, 5]
        result = confidence_interval(data, confidence_level=0.95)
        
        # Should have these keys
        assert 'mean' in result
        assert 'std' in result
        assert 'confidence_level' in result
        assert 'lower_bound' in result
        assert 'upper_bound' in result
        assert 'margin_of_error' in result
        
        # Mean should be correct
        assert abs(result['mean'] - 3.0) < 1e-10
        
        # Confidence interval should contain the mean
        assert result['lower_bound'] <= result['mean'] <= result['upper_bound']
    
    def test_confidence_interval_invalid_confidence_level(self):
        """Test confidence interval with invalid confidence level."""
        data = [1, 2, 3, 4, 5]
        with pytest.raises(ValidationError):
            confidence_interval(data, confidence_level=0)
        
        with pytest.raises(ValidationError):
            confidence_interval(data, confidence_level=1)
    
    def test_confidence_interval_insufficient_data(self):
        """Test confidence interval with insufficient data."""
        with pytest.raises(ValidationError):
            confidence_interval([1])


class TestZScore:
    """Test z-score calculation."""
    
    def test_z_score_basic(self):
        """Test z-score calculation."""
        # z-score of 5 with mean=3, std=2 should be 1
        result = z_score(5, 3, 2)
        expected = 1.0
        assert abs(result - expected) < 1e-10
    
    def test_z_score_invalid_std(self):
        """Test z-score with invalid standard deviation."""
        with pytest.raises(ValidationError):
            z_score(5, 3, 0)
        
        with pytest.raises(ValidationError):
            z_score(5, 3, -1)


class TestPercentile:
    """Test percentile calculation."""
    
    def test_percentile_basic(self):
        """Test percentile calculation."""
        data = [1, 2, 3, 4, 5]
        
        # 50th percentile should be median
        result = percentile(data, 50)
        expected = 3.0
        assert abs(result - expected) < 1e-10
        
        # 0th percentile should be minimum
        result = percentile(data, 0)
        expected = 1.0
        assert abs(result - expected) < 1e-10
        
        # 100th percentile should be maximum
        result = percentile(data, 100)
        expected = 5.0
        assert abs(result - expected) < 1e-10
    
    def test_percentile_invalid_percentile(self):
        """Test percentile with invalid percentile value."""
        data = [1, 2, 3, 4, 5]
        with pytest.raises(ValidationError):
            percentile(data, -1)
        
        with pytest.raises(ValidationError):
            percentile(data, 101)
    
    def test_percentile_empty_data(self):
        """Test percentile with empty data."""
        with pytest.raises(ValidationError):
            percentile([], 50)


if __name__ == "__main__":
    pytest.main([__file__])
