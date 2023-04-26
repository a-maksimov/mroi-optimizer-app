import streamlit as st


def about_page():
    st.markdown(
        """
    # OBJECTIVES OF THE MEDIA PLANNING APP
    
    To understand how much additional spending is reasonable for a media/ brand/ location, etc.
    
    To understand how to get a better business performance for a given total marketing budget.
    
    To understand how much additional marketing investment is required for a given performance target.
    
    # USEFUL TERMS What is Granularity? Granularity represents the overall design of the media activities. It can be 
    platforms like Facebook, Instagram, TV, etc. It can be different formats like video, display, etc.
    
    What is Contribution? Contribution represents the amount of sales volume which is the outcome of media 
    activities. Contribution is calculated through marketing mix modeling.
    
    What is a Response Curve? Response curves represent the relation between the amount of money spent on a media and 
    the contribution attributable to that media. The parameters to build the response curves are calculated through 
    marketing mix modeling.
    
    What is "Simulate" or "What-If" scenario? Suppose you have a new media budget for this year. And you want to 
    continue the past periods’ media spending pattern. You can do the same by entering the new budget and clicking on 
    Simulate.
    
    What is Spend Based Optimisation? Simulation may not result in maximum sales volume. Because past budget 
    allocation might not be the best one. To get the best allocation for a given budget, select Spend based 
    Optimisation.
    
    What is Goal Based Optimisation? Suppose, last year the uplift volume was 167 thousands kg. This year, 
    you plan to achieve 180 thousands kg. If you use Goal Based Optimisation, you will get the optimal budget 
    allocation to achieve that target.
    
    # STEPS TO RUN THE APP
    1. Go to the Media Specifications tab.
    2. Select granularity and periodicity.
    3. Select different items of granularity.
    4. Click SUBMIT to see the past performance.
    5. Click on MEDIA PLANNING button to move to the planning tab.
    6. Add a budget and click SIMULATE to get budget allocation based on past.
    7. Click on SPEND BASED OPTIMISATION button to get the optimised budget allocation for the same budget.
    8. To achieve a business performance target, enter the target and click on GOAL BASED OPTIMISATION.
    
    # OUTPUTS
    
    COMPARISON OVER PERIODICITY is a plot to compare the simulated (what-if) and the optimised spending over the 
    selected periodicity (weekly, monthly, etc.).
    
    COMPARISON OVER GRANULARITY is a collection of plots comparing simulated (what-if) and the optimised scenarios on 
    spending and uplift for different granularity.
    
    SPEND/ GOAL BASED OPTIMISATION is the comparison between the simulated (what-if) and optimised scenarios in a 
    tabular format."""
    )
    return about_page
