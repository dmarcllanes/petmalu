from fasthtml.common import *

def home_page():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Title('PetNourish - Pet Nutrition & Wellness'),
        Link(rel='stylesheet', href='/css/homepage.css')
    ),
    Body(
        Nav(
            Div(
                Div(
                    Span('🐾', cls='logo-icon'),
                    Span('PetNourish', cls='logo-text'),
                    cls='nav-brand'
                ),
                Ul(
                    Li(
                        A('Features', href='#features')
                    ),
                    Li(
                        A('How It Works', href='#how-it-works')
                    ),
                    Li(
                        A('Pricing', href='#pricing')
                    ),
                    Li(
                        A('Get Started', href='/login', cls='nav-cta')
                    ),
                    cls='nav-links'
                ),
                cls='container'
            ),
            cls='navbar'
        ),
        Section(
            Div(
                Div(
                    H1('Nourish Your Pet with Precision', cls='hero-title'),
                    P('The science-backed way to calculate perfect portions, track wellness, and keep your pet thriving', cls='hero-subtitle'),
                    Div(
                        A('Start Free Today', href='/login', cls='btn btn-primary btn-lg'),
                        Button('See How It Works', cls='btn btn-secondary btn-lg'),
                        cls='hero-cta-group'
                    ),
                    cls='hero-content'
                ),
                Div(
                    Div(
                        Div(
                            Span('2,450', cls='metric-value'),
                            Span('Daily Calories', cls='metric-label'),
                            cls='metric'
                        ),
                        Div(
                            Span('65%', cls='metric-value'),
                            Span('Portion Optimized', cls='metric-label'),
                            cls='metric'
                        ),
                        cls='hero-card'
                    ),
                    cls='hero-visual'
                ),
                cls='container'
            ),
            cls='hero'
        ),
        Section(
            Div(
                H2('Why Pet Nutrition Matters', cls='section-title'),
                Div(
                    Div(
                        Div('⚠️', cls='problem-icon'),
                        H3('Overfeeding is Common'),
                        P('60% of pets are overweight, leading to health complications and shortened lifespans'),
                        cls='problem-item'
                    ),
                    Div(
                        Div('🤔', cls='problem-icon'),
                        H3('Portion Confusion'),
                        P("Pet owners struggle to determine correct feeding amounts for their unique pet's needs"),
                        cls='problem-item'
                    ),
                    Div(
                        Div('🔍', cls='problem-icon'),
                        H3('Hidden Allergies'),
                        P('Tracking ingredient allergies and reactions is complex without the right tools'),
                        cls='problem-item'
                    ),
                    cls='problem-grid'
                ),
                cls='container'
            ),
            cls='problem'
        ),
        Section(
            Div(
                H2('Powerful Features for Pet Wellness', cls='section-title'),
                Div(
                    Div(
                        Div('🧮', cls='feature-icon'),
                        H3('Calorie Calculator'),
                        P('AI-powered calculations based on breed, age, weight, and activity level for precise daily calorie needs'),
                        cls='feature-card'
                    ),
                    Div(
                        Div('🍽️', cls='feature-icon'),
                        H3('Portion Optimizer'),
                        P("Automatic portion recommendations tailored to your pet's specific requirements and feeding schedule"),
                        cls='feature-card'
                    ),
                    Div(
                        Div('📊', cls='feature-icon'),
                        H3('Weight Tracking'),
                        P('Monitor weight trends over time with visual charts and trend analysis to ensure optimal health'),
                        cls='feature-card'
                    ),
                    Div(
                        Div('⚡', cls='feature-icon'),
                        H3('Allergy Alerts'),
                        P('Track ingredient sensitivities and get instant alerts when problematic items appear in foods'),
                        cls='feature-card'
                    ),
                    Div(
                        Div('💊', cls='feature-icon'),
                        H3('Supplement Reminders'),
                        P("Schedule and manage supplement doses with smart reminders to support your pet's wellness goals"),
                        cls='feature-card'
                    ),
                    Div(
                        Div('📱', cls='feature-icon'),
                        H3('Mobile Companion'),
                        P('Access all features on-the-go with our intuitive mobile app for seamless pet care management'),
                        cls='feature-card'
                    ),
                    cls='features-grid'
                ),
                cls='container'
            ),
            id='features',
            cls='features'
        ),
        Section(
            Div(
                H2('Three Simple Steps to Better Pet Health', cls='section-title'),
                Div(
                    Div(
                        Div('1', cls='step-number'),
                        H3("Create Your Pet's Profile"),
                        P("Input your pet's breed, age, weight, and activity level. Our system learns your pet's unique needs in seconds."),
                        cls='step'
                    ),
                    Div(
                        Div('2', cls='step-number'),
                        H3('Get Personalized Recommendations'),
                        P('Receive daily calorie targets, portion sizes, and feeding schedules customized specifically for your pet.'),
                        cls='step'
                    ),
                    Div(
                        Div('3', cls='step-number'),
                        H3('Track & Optimize'),
                        P('Log meals, track weight, monitor allergies, and watch your pet thrive with data-driven insights.'),
                        cls='step'
                    ),
                    cls='steps-grid'
                ),
                cls='container'
            ),
            id='how-it-works',
            cls='how-it-works'
        ),
        Section(
            Div(
                H2('Simple, Transparent Pricing', cls='section-title'),
                Div(
                    Div(
                        Div(
                            H3('Free'),
                            Div(
                                '$0',
                                Span('/month'),
                                cls='pricing-price'
                            ),
                            cls='pricing-header'
                        ),
                        Ul(
                            Li('✓ One pet profile'),
                            Li('✓ Basic calorie calculator'),
                            Li('✓ Manual weight tracking'),
                            Li('✗ Allergy alerts'),
                            Li('✗ Supplement reminders'),
                            cls='pricing-features'
                        ),
                        Button('Start Free', cls='btn btn-outline'),
                        cls='pricing-card'
                    ),
                    Div(
                        Div('Most Popular', cls='pricing-badge'),
                        Div(
                            H3('Pro'),
                            Div(
                                '$9.99',
                                Span('/month'),
                                cls='pricing-price'
                            ),
                            cls='pricing-header'
                        ),
                        Ul(
                            Li('✓ Up to 3 pet profiles'),
                            Li('✓ Advanced calorie calculator'),
                            Li('✓ Automated weight tracking'),
                            Li('✓ Allergy alerts & management'),
                            Li('✗ Supplement reminders'),
                            cls='pricing-features'
                        ),
                        Button('Start Pro Trial', cls='btn btn-primary'),
                        cls='pricing-card featured'
                    ),
                    Div(
                        Div(
                            H3('Premium'),
                            Div(
                                '$19.99',
                                Span('/month'),
                                cls='pricing-price'
                            ),
                            cls='pricing-header'
                        ),
                        Ul(
                            Li('✓ Unlimited pet profiles'),
                            Li('✓ AI-powered optimizer'),
                            Li('✓ Advanced analytics & reports'),
                            Li('✓ Allergy alerts & management'),
                            Li('✓ Smart supplement reminders'),
                            cls='pricing-features'
                        ),
                        Button('Start Premium Trial', cls='btn btn-outline'),
                        cls='pricing-card'
                    ),
                    cls='pricing-grid'
                ),
                cls='container'
            ),
            id='pricing',
            cls='pricing'
        ),
        Section(
            Div(
                H2("Your Pet's Health, Our Priority", cls='section-title'),
                Div(
                    Div(
                        H3('Science-Backed Recommendations'),
                        P('PetNourish is built on veterinary nutrition science and continuously updated with the latest pet wellness research.'),
                        Ul(
                            Li('📋 Developed with certified veterinary nutritionists'),
                            Li('🔬 Based on peer-reviewed nutritional studies'),
                            Li('⚖️ Complies with AAFCO nutrition standards'),
                            Li('🛡️ Not a replacement for veterinary care'),
                            cls='safety-list'
                        ),
                        cls='safety-text'
                    ),
                    Div(
                        Div(
                            P('"PetNourish helps me understand my dog\'s nutrition better, but I always consult my vet for medical concerns."', cls='highlight-text'),
                            P('— Sarah M., Pet Owner', cls='highlight-author'),
                            cls='highlight-card'
                        ),
                        cls='safety-highlight'
                    ),
                    cls='safety-content'
                ),
                cls='container'
            ),
            id='safety',
            cls='safety'
        ),
        Section(
            Div(
                H2("Ready to Transform Your Pet's Wellness?"),
                P('Join thousands of pet owners who are feeding smarter and watching their pets thrive'),
                A('Start Your Free Account Today', href='/login', cls='btn btn-primary btn-lg'),
                P('No credit card required • 14-day free trial available', cls='cta-note'),
                cls='container'
            ),
            cls='final-cta'
        ),
        Footer(
            Div(
                Div(
                    Div(
                        H4('PetNourish'),
                        P('Precision nutrition for every pet'),
                        cls='footer-section'
                    ),
                    Div(
                        H4('Product'),
                        Ul(
                            Li(
                                A('Features', href='#features')
                            ),
                            Li(
                                A('Pricing', href='#pricing')
                            ),
                            Li(
                                A('Blog', href='#')
                            )
                        ),
                        cls='footer-section'
                    ),
                    Div(
                        H4('Legal'),
                        Ul(
                            Li(
                                A('Privacy Policy', href='#')
                            ),
                            Li(
                                A('Terms of Service', href='#')
                            ),
                            Li(
                                A('Disclaimer', href='#')
                            )
                        ),
                        cls='footer-section'
                    ),
                    cls='footer-content'
                ),
                Div(
                    P('© 2025 PetNourish. All rights reserved.'),
                    cls='footer-bottom'
                ),
                cls='container'
            ),
            cls='footer'
        ),
        Script(src='/js/homepage.js')
    ),
    lang='en'
)