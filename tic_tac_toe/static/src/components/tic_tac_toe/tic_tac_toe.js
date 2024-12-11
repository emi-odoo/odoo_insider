import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

function _areEqual(arr1, arr2) {
    return JSON.stringify(arr1) == JSON.stringify(arr2);
}

export class TicTacToe extends Component {
    static template = "tic_tac_toe.TicTacToe";
    static props = {
        ...standardFieldProps,
    }

    setup() {
        this.board = useState([Array(3).fill(""), Array(3).fill(""), Array(3).fill("")]);
        this.player1 = this.props.record.data.player1[1];
        this.player2 = this.props.record.data.player2[1];
        this.currentPlayer = this.player1;
        this.winner =  "";
    }

    play(row, column) {
        if(this.winner != "") {
            this.board = [Array(3).fill(""), Array(3).fill(""), Array(3).fill("")]
            return true;
        }

        const player = this.currentPlayer;

        if (!this.board[row][column]) {
            this.board[row][column] = player;
        }

        this.currentPlayer = player == this.player1 ? this.player2 : this.player1;
        if(this._checkWinner(this.player1)) {
            this.winner = this.player1;
        }
        else if(this._checkWinner(this.player2)) {
            this.winner = this.player2;
        }
    }

    _checkWinner(player) {
        const fullRow = Array(3).fill(player);

        if (this.board.some(col => _areEqual(col, fullRow))) {
            return true;
        }

        for (let i = 0; i < 3; i++) {
            if (_areEqual(this.board.map(x => x[i]), fullRow)) {
                return true;
            }
        }

        let diagonal = true;
        for (let j = 0; j < 3; j++) {
            if(this.board[j][j] != player) {
                diagonal = false;
                break;
            }
        }
        if (diagonal) return true;

        diagonal = true;
        for (let k = 0; k < 3; k++) {
            if(this.board[k][2 - k] != player) {
                diagonal = false;
                break;
            }
        }
        if (diagonal) return true;

        return false;
    }
}

registry.category("view_widgets").add("tic_tac_toe", { component: TicTacToe });
