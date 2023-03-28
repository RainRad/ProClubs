CREATE TABLE "clubs" (
    "pull_time" timestamp   NOT NULL,
    "club_name" varchar(25)   NOT NULL,
    "active" varchar(5)   NOT NULL,
    "console" varchar(10)   NOT NULL,
    "club_id" integer   NOT NULL,
    "division" integer   NOT NULL,
    "ten_match_record" varchar(10)   NOT NULL,
    "total_games" integer   NOT NULL,
    "wins" integer   NOT NULL,
    "losses" integer   NOT NULL,
    "draws" integer   NOT NULL,
    "goals_scored" integer   NOT NULL,
    "goals_per_match" float   NOT NULL,
    "goals_conceded" integer   NOT NULL,
    "goals_conceded_per_match" float   NOT NULL,
    "goal_difference" integer   NOT NULL,
    "promotions" integer   NOT NULL,
    "holds" integer   NOT NULL,
    "relegations" integer   NOT NULL,
    "best_season_div" integer   NOT NULL,
    "best_season_points" integer   NOT NULL,
    "region" varchar(25)   NOT NULL,
    "stadium" varchar(50)   NOT NULL,
    "total_rank_points" integer   NOT NULL,
    "league_points" integer   NOT NULL,
    "cup_points" integer   NOT NULL,
    "div_1_titles" integer   NOT NULL,
    "other_div_titles" integer   NOT NULL,
    "total_trophies" integer   NOT NULL,
    CONSTRAINT "pk_clubs" PRIMARY KEY (
        "club_id"
     )
);

CREATE TABLE "games" (
    "pull_time" timestamp   NOT NULL,
    "game_id" bigint   NOT NULL,
    "console" varchar(10)   NOT NULL,
    "winning_club" varchar(25)   NOT NULL,
    "h_club" varchar(25)   NOT NULL,
    "h_club_id" integer   NOT NULL,
    "h_goals" integer   NOT NULL,
    "h_shots" integer   NOT NULL,
    "h_shot_percent" float   NOT NULL,
    "h_passes_made" integer   NOT NULL,
    "h_pass_attempts" integer   NOT NULL,
    "h_pass_percent" float   NOT NULL,
    "h_tackles_made" integer   NOT NULL,
    "h_tackle_attempts" integer   NOT NULL,
    "h_tackle_percent" float   NOT NULL,
    "h_red_cards" integer   NOT NULL,
    "h_players_in_match" integer   NOT NULL,
    "h_forward" integer   NOT NULL,
    "h_midfielder" integer   NOT NULL,
    "h_defender" integer   NOT NULL,
    "h_goalkeeper" integer   NOT NULL,
    "h_any" integer   NOT NULL,
    "h_season" integer   NOT NULL,
    "h_round" integer   NOT NULL,
    "opp_club" varchar(25)   NOT NULL,
    "opp_club_id" integer   NOT NULL,
    "opp_goals" integer   NOT NULL,
    "opp_shots" integer   NOT NULL,
    "opp_shot_percent" float   NOT NULL,
    "opp_passes_made" integer   NOT NULL,
    "opp_pass_attempts" integer   NOT NULL,
    "opp_pass_percent" float   NOT NULL,
    "opp_tackles_made" integer   NOT NULL,
    "opp_tackle_attempts" integer   NOT NULL,
    "opp_tackle_percent" float   NOT NULL,
    "opp_red_cards" integer   NOT NULL,
    "opp_players_in_match" integer   NOT NULL,
    "opp_forward" integer   NOT NULL,
    "opp_midfielder" integer   NOT NULL,
    "opp_defender" integer   NOT NULL,
    "opp_goalkeeper" integer   NOT NULL,
    "opp_any" integer   NOT NULL,
    "opp_season" integer   NOT NULL,
    "opp_round" integer   NOT NULL,
    CONSTRAINT "pk_games" PRIMARY KEY (
        "game_id"
     )
);

CREATE TABLE "single_match_player_performance" (
    "id" serial   NOT NULL,
    "pull_time" timestamp   NOT NULL,
    "game_id" integer   NOT NULL,
    "name" varchar(25)   NOT NULL,
    "club" varchar(25)   NOT NULL,
    "position" varchar(25)   NOT NULL,
    "rating" float   NOT NULL,
    "motm" varchar(5)   NOT NULL,
    "goals" integer   NOT NULL,
    "shots" integer   NOT NULL,
    "shot_percent" float   NOT NULL,
    "assist" integer   NOT NULL,
    "passes_made" integer   NOT NULL,
    "pass_attempts" integer   NOT NULL,
    "pass_percent" float   NOT NULL,
    "tackles_made" integer   NOT NULL,
    "tackle_attempts" integer   NOT NULL,
    "tackle_percent" float   NOT NULL,
    "red_card" integer   NOT NULL,
    "gk_saves" integer   NOT NULL,
    CONSTRAINT "pk_single_match_player_performance" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "games" ADD CONSTRAINT "fk_games_h_club_id" FOREIGN KEY("h_club_id")
REFERENCES "clubs" ("club_id");

ALTER TABLE "games" ADD CONSTRAINT "fk_games_opp_club_id" FOREIGN KEY("opp_club_id")
REFERENCES "clubs" ("club_id");

ALTER TABLE "single_match_player_performance" ADD CONSTRAINT "fk_single_match_player_performance_game_id" FOREIGN KEY("game_id")
REFERENCES "games" ("game_id");