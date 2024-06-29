# E-Auction

## Description
E-Auction is an eBay-like e-commerce auction platform where users can create auction listings, place bids, comment on listings, and manage their watchlist. This application was developed as part of my [**CS50W**](https://cs50.harvard.edu/web/2020/) **`Second Project`** in 2023. You can explore its development on [me/50](https://github.com/me50/emads22/tree/web50/projects/2020/x/commerce) repository.

---

## Features

1. **Create Listing**
   - Users can create new listings with title, description, and starting bid.
   - Optional: Image URL and category selection.

2. **Active Listings Page**
   - Displays all active auction listings with title, description, current price, and photo (if available).

3. **Listing Page**
   - Provides detailed listing information including current price.
   - Watchlist toggle (for signed-in users).
   - Bid form (available if signed-in and meets bid criteria).
   - Close auction option (for listing creators).

4. **Watchlist**
   - Signed-in users can add/remove listings to/from their watchlist.
   - View all listings on their watchlist.

5. **Categories**
   - View a list of all listing categories.
   - Click on a category to view active listings within that category.

6. **Admin Interface**
   - Django admin interface for managing listings, comments, and bids.
   
---

## Setup
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install dependencies with `pip install -r requirements.txt`.
4. Configure database settings in `settings.py`.
5. Run Django development server: `python manage.py runserver`.

## Usage
1. Access the web app through your browser at `http://127.0.0.1:8000/`.
2. Register for an account or log in to start using the auction features.
3. Explore, bid, comment, and manage your watchlist for a complete e-commerce experience.

## Example
#### Rami's User Profile:
- **Username**: `rami`
- **Password**: `123456` 

Rami actively participates in E-Auction, engaging in bidding, managing his watchlist, and commenting on listings. Explore his activity on the platform to see his current bids and watchlist selections.

## Contributing
Contributions are welcome! Here are ways to contribute:
- Report bugs or issues.
- Suggest new features or improvements.
- Submit pull requests with enhancements.

## Author
- Emad &nbsp; E>
  
  [<img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" width="150">](https://github.com/emads22)

## License
This project is licensed under the MIT License, which grants permission for free use, modification, distribution, and sublicense of the code, provided that the copyright notice (attributed to [emads22](https://github.com/emads22)) and permission notice are included in all copies or substantial portions of the software. This license is permissive and allows users to utilize the code for both commercial and non-commercial purposes.

Please see the [LICENSE](LICENSE) file for more details.
