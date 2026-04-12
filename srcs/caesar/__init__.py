"""Caesar Cipher Package with Brute Force Attacks"""

from .caesar import (
    encrypt,
    decrypt,
    brute_force_exhaustive,
    brute_force_exhaustive_display,
    brute_force_frequency_analysis,
    brute_force_frequency_analysis_top_n,
    brute_force_frequency_analysis_display,
    brute_force_frequency_analysis_bigram,
    brute_force_frequency_analysis_bigram_top_n,
    brute_force_frequency_analysis_bigram_display,
    analyze_frequency,
    analyze_bigram_frequency,
    standard_english_freq,
    standard_english_bigram_freq,
    chi_squared_test,
    recommend_analysis_method,
    encrypt_file,
    decrypt_file
)

__all__ = [
    'encrypt',
    'decrypt',
    'brute_force_exhaustive',
    'brute_force_exhaustive_display',
    'brute_force_frequency_analysis',
    'brute_force_frequency_analysis_top_n',
    'brute_force_frequency_analysis_display',
    'brute_force_frequency_analysis_bigram',
    'brute_force_frequency_analysis_bigram_top_n',
    'brute_force_frequency_analysis_bigram_display',
    'analyze_frequency',
    'analyze_bigram_frequency',
    'standard_english_freq',
    'standard_english_bigram_freq',
    'chi_squared_test',
    'recommend_analysis_method',
    'encrypt_file',
    'decrypt_file'
]

__version__ = '2.0.0'
