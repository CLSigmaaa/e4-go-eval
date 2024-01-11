package main

import (
	"fmt"
	"math/rand"
)

type Arme struct {
	Nom         string
	DegatMax    int
	DistanceMax int
}

type Item struct {
	Nom string
}

type Personnage struct {
	X             int
	Y             int
	Nom           string
	PointsVie     int
	PointsAttaque int
	PointsDefense int
	Arme          Arme
	Inventaire    []Item
}

type IPersonnage interface {
	Deplacer()
	Attaquer()
	Recuperer()
	Mourir()
}

func (p *Personnage) Deplacer(direction string) {
	if direction == "haut" {
		p.Y--
	} else if direction == "bas" {
		p.Y++
	} else if direction == "gauche" {
		p.X--
	} else if direction == "droite" {
		p.X++
	} else {
		fmt.Println("Mauvaise direction")
	}
}

func (p *Personnage) Attaquer(cible Personnage) {
	cible.PointsVie -= p.PointsAttaque
	fmt.Println(p.Nom, "attaque", cible.Nom, "et lui inflige", p.PointsAttaque, "points de dégats")
	fmt.Println()
	if cible.PointsVie <= 0 {
		cible.Mourir()
		fmt.Println(cible.Nom, "est mort")
	} else {
		fmt.Println(cible.Nom, "a encore", cible.PointsVie, "points de vie")
	}
}

func (p *Personnage) Recuperer(item Item) {
	p.Inventaire = append(p.Inventaire, item)
	fmt.Println(p.Nom, "a récupéré", item.Nom)
}

func (p *Personnage) Mourir() {
	fmt.Println(p.Nom, "est mort")
}

type Magicien struct {
	Personnage
}

type Chevalier struct {
	Personnage
}

type Gobelin struct {
	Personnage
}

type Orc struct {
	Personnage
}

type Elf struct {
	Personnage
}

type Nain struct {
	Personnage
}

type Case struct {
	Type    string
	Occupe  bool
	Symbole string
}

type EntityManager struct {
	maxMagicien  int
	maxChevalier int
	maxGobelin   int
	maxOrc       int
	maxElf       int
	maxNain      int

	defaultMagicien  Magicien
	defaultChevalier Chevalier
	defaultGobelin   Gobelin
	defaultOrc       Orc
	defaultElf       Elf
	defaultNain      Nain

	magiciens  []Magicien
	chevaliers []Chevalier
	gobelins   []Gobelin
	orcs       []Orc
	elfs       []Elf
	nains      []Nain
}

type IEntityManager interface {
	GenererPersonnage()
}

func (e *EntityManager) GenererPersonnage() {
	var magicien Magicien
	magicien.Nom = "Magicien"
	magicien.PointsVie = 100
	magicien.PointsAttaque = 10
	magicien.PointsDefense = 10
	magicien.Arme = Arme{Nom: "Baton", DegatMax: 10, DistanceMax: 1}

	var chevalier Chevalier
	chevalier.Nom = "Chevalier"
	chevalier.PointsVie = 100
	chevalier.PointsAttaque = 10
	chevalier.PointsDefense = 10
	chevalier.Arme = Arme{Nom: "Epée", DegatMax: 10, DistanceMax: 1}

	var gobelin Gobelin
	gobelin.Nom = "Gobelin"
	gobelin.PointsVie = 100
	gobelin.PointsAttaque = 10
	gobelin.PointsDefense = 10
	gobelin.Arme = Arme{Nom: "Dague", DegatMax: 10, DistanceMax: 1}

	var orc Orc
	orc.Nom = "Orc"
	orc.PointsVie = 100
	orc.PointsAttaque = 10
	orc.PointsDefense = 10
	orc.Arme = Arme{Nom: "Hache", DegatMax: 10, DistanceMax: 1}

	var elf Elf
	elf.Nom = "Elf"
	elf.PointsVie = 100
	elf.PointsAttaque = 10
	elf.PointsDefense = 10
	elf.Arme = Arme{Nom: "Arc", DegatMax: 10, DistanceMax: 1}

	var nain Nain
	nain.Nom = "Nain"
	nain.PointsVie = 100
	nain.PointsAttaque = 10
	nain.PointsDefense = 10
	nain.Arme = Arme{Nom: "Hache", DegatMax: 10, DistanceMax: 1}

	e.defaultMagicien = magicien
	e.defaultChevalier = chevalier
	e.defaultGobelin = gobelin
	e.defaultOrc = orc
	e.defaultElf = elf
	e.defaultNain = nain
}

type Carte struct {
	Cases         [][]Case
	Longueur      int
	Largeur       int
	EntityManager EntityManager
}

type ICarte interface {
	GenererCarte()
	AfficherCarte()
}

func (c *Carte) GenererCarte() {

	c.Cases = make([][]Case, c.Longueur)
	for i := 0; i < c.Longueur; i++ {
		c.Cases[i] = make([]Case, c.Largeur)
		for j := 0; j < c.Largeur; j++ {
			if i == 0 || i == c.Longueur-1 || j == 0 || j == c.Largeur-1 {
				c.Cases[i][j] = Case{Type: "Wall", Occupe: false, Symbole: "⬛"}
			} else if rand.Intn(12) < 3 {
				c.Cases[i][j] = Case{Type: "Wall", Occupe: false, Symbole: "⬛"}
			} else if rand.Intn(400) < 3 && (len(c.EntityManager.chevaliers) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "🤺"}
				c.EntityManager.maxChevalier++
				c.EntityManager.defaultChevalier.X = i
				c.EntityManager.defaultChevalier.Y = j
				c.EntityManager.chevaliers = append(c.EntityManager.chevaliers, c.EntityManager.defaultChevalier)
			} else if rand.Intn(800) < 3 && (len(c.EntityManager.magiciens) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "🧙"}
				c.EntityManager.maxMagicien++
				c.EntityManager.defaultMagicien.X = i
				c.EntityManager.defaultMagicien.Y = j
				c.EntityManager.magiciens = append(c.EntityManager.magiciens, c.EntityManager.defaultMagicien)
			} else if rand.Intn(1200) < 3 && (len(c.EntityManager.gobelins) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "👺"}
				c.EntityManager.maxGobelin++
				c.EntityManager.defaultGobelin.X = i
				c.EntityManager.defaultGobelin.Y = j
				c.EntityManager.gobelins = append(c.EntityManager.gobelins, c.EntityManager.defaultGobelin)
			} else if rand.Intn(42) < 3 && (len(c.EntityManager.orcs) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "👹"}
				c.EntityManager.maxOrc++
				c.EntityManager.defaultOrc.X = i
				c.EntityManager.defaultOrc.Y = j
				c.EntityManager.orcs = append(c.EntityManager.orcs, c.EntityManager.defaultOrc)
			} else if rand.Intn(450) < 3 && (len(c.EntityManager.elfs) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "🧟"}
				c.EntityManager.maxElf++
				c.EntityManager.elfs = append(c.EntityManager.elfs, c.EntityManager.defaultElf)
			} else if rand.Intn(200) < 3 && (len(c.EntityManager.nains) < 1) {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: true, Symbole: "🧝"}
				c.EntityManager.maxNain++
				c.EntityManager.defaultNain.X = i
				c.EntityManager.defaultNain.Y = j
				c.EntityManager.nains = append(c.EntityManager.nains, c.EntityManager.defaultNain)
			} else {
				c.Cases[i][j] = Case{Type: "Plaine", Occupe: false, Symbole: "🟩"}
			}
		}
	}
}

func (c *Carte) AfficherCarte() {
	for i := 0; i < c.Longueur; i++ {
		for j := 0; j < c.Largeur; j++ {
			fmt.Print(c.Cases[i][j].Symbole)
		}
		fmt.Println()
	}
}

func main() {
	var entityManager EntityManager
	entityManager.maxMagicien = 1
	entityManager.maxChevalier = 1
	entityManager.maxGobelin = 1
	entityManager.maxOrc = 1
	entityManager.maxElf = 1
	entityManager.maxNain = 1
	entityManager.GenererPersonnage()

	var carte Carte
	carte.Longueur = 20
	carte.Largeur = 40
	carte.EntityManager = entityManager

	carte.GenererCarte()
	carte.AfficherCarte()

	// fmt.Println(carte.Cases)

}
